#!/usr/bin/env python3
from __future__ import annotations

import configparser
import datetime as dt
import json
import math
import os
from pathlib import Path
import re
import shutil
import sqlite3
import stat
import subprocess
import sys
import tempfile
import threading
import time
import zipfile
from dataclasses import dataclass
from typing import Callable, Optional

WEB_MERCATOR_HALF = 20037508.342789244
WEB_MERCATOR_RES_Z0 = 156543.03392804097
ProgressCallback = Callable[[str, str, Optional[float]], None]

class RastaError(RuntimeError):
    pass

class BuildCancelled(RastaError):
    pass

@dataclass(frozen=True)
class Config:
    base_dir: Path
    qgis_install_dir: Path
    expected_qgis_version: str
    dpi: int
    antialias: bool
    tile_format: int
    quality: int
    metatile_size: int
    default_min_zoom: int
    default_max_zoom: int
    synthetic_meters_per_pixel: float
    synthetic_anchor_lon: float
    synthetic_anchor_lat: float
    warning_tile_count: int

@dataclass(frozen=True)
class RasterInfo:
    path: Path
    width: int
    height: int
    driver: str
    has_crs: bool
    has_geotransform: bool
    mode_suggested: str

@dataclass(frozen=True)
class BuildResult:
    input_file: Path
    mode: str
    output_mode: str
    mbtiles_file: Optional[Path]
    tpkx_file: Optional[Path]
    tile_count: int
    min_zoom: int
    max_zoom: int
    bundle_count: int
    elapsed_seconds: float


def load_config(base_dir: Path) -> Config:
    path = base_dir / "Rasta_Config.ini"
    cp = configparser.ConfigParser()
    if not path.is_file():
        raise RastaError(f"Configuration file is missing: {path}")
    cp.read(path, encoding="utf-8")
    q = cp["QGIS"]
    p = cp["PYRAMID"]
    return Config(
        base_dir=base_dir,
        qgis_install_dir=Path(os.path.expandvars(q.get("qgis_install_dir", r"C:\Program Files\QGIS 3.44.9"))),
        expected_qgis_version=q.get("expected_qgis_version", "3.44.9").strip(),
        dpi=p.getint("dpi", 96),
        antialias=p.getboolean("antialias", True),
        tile_format=p.getint("tile_format", 0),
        quality=p.getint("quality", 75),
        metatile_size=p.getint("metatile_size", 4),
        default_min_zoom=p.getint("default_min_zoom", 0),
        default_max_zoom=p.getint("default_max_zoom", 18),
        synthetic_meters_per_pixel=p.getfloat("synthetic_meters_per_pixel", 1.0),
        synthetic_anchor_lon=p.getfloat("synthetic_anchor_lon", -80.0),
        synthetic_anchor_lat=p.getfloat("synthetic_anchor_lat", 30.0),
        warning_tile_count=p.getint("warning_tile_count", 100000),
    )


def explorer_size(size: int) -> str:
    return f"{(max(0, int(size)) + 1023) // 1024:,} KB"


def _hidden_flags(new_group: bool = False):
    if os.name != "nt":
        return 0, None
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    if new_group:
        flags |= getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0
    return flags, si


def terminate_tree(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        try:
            subprocess.run(
                ["taskkill", "/PID", str(proc.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
                timeout=10,
            )
            return
        except Exception:
            pass
    try:
        proc.terminate()
        proc.wait(timeout=5)
    except Exception:
        try:
            proc.kill()
        except Exception:
            pass


def qgis_desktop_running() -> bool:
    if os.name != "nt":
        return False
    try:
        out = subprocess.run(
            ["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), timeout=8,
        ).stdout.lower()
    except Exception:
        return False
    return any(name in out for name in ('"qgis-bin.exe"', '"qgis.exe"'))


def _find_first(root: Path, names: tuple[str, ...]) -> Path:
    candidates = []
    for name in names:
        candidates.extend([root / "bin" / name, root / name])
    for p in candidates:
        if p.is_file():
            return p
    if root.is_dir():
        lowers = {n.lower() for n in names}
        for p in root.rglob("*"):
            if p.is_file() and p.name.lower() in lowers:
                return p
    raise RastaError(f"Required QGIS tool not found under {root}: {', '.join(names)}")


def find_tools(config: Config) -> dict[str, Path]:
    root = config.qgis_install_dir
    if not root.exists():
        raise RastaError(f"QGIS install folder not found: {root}")
    return {
        "qgis_process": _find_first(root, ("qgis_process-qgis-ltr.bat", "qgis_process-qgis.bat", "qgis_process.bat", "qgis_process-qgis-ltr.exe", "qgis_process-qgis.exe", "qgis_process.exe")),
        "python_qgis": _find_first(root, ("python-qgis.bat", "python-qgis-ltr.bat")),
        "gdalinfo": _find_first(root, ("gdalinfo.exe", "gdalinfo")),
        "gdal_translate": _find_first(root, ("gdal_translate.exe", "gdal_translate")),
        "gdaladdo": _find_first(root, ("gdaladdo.exe", "gdaladdo")),
    }


def command_for(executable: Path, args: list[str]) -> list[str]:
    if os.name == "nt" and executable.suffix.lower() in {".bat", ".cmd"}:
        return [os.environ.get("COMSPEC", "cmd.exe"), "/d", "/c", "call", str(executable), *args]
    return [str(executable), *args]


def _run_capture_split(cmd: list[str], timeout: int = 30) -> tuple[int, str, str]:
    """Run a short command while preserving stdout and stderr separately.

    Machine-readable tools such as ``gdalinfo -json`` write JSON to stdout and
    diagnostics/warnings to stderr.  Never concatenate the two before parsing.
    """
    flags, si = _hidden_flags()
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                       creationflags=flags, startupinfo=si, timeout=timeout)
    return p.returncode, (p.stdout or ""), (p.stderr or "")


def _run_capture(cmd: list[str], timeout: int = 30) -> tuple[int, str]:
    rc, stdout, stderr = _run_capture_split(cmd, timeout=timeout)
    return rc, stdout + stderr


def _parse_json_payload(text: str) -> dict:
    """Parse the first JSON object in text and tolerate harmless trailing output.

    Some GDAL builds or image codecs can emit a warning after the JSON payload.
    ``json.loads`` rejects that with ``Extra data`` even though the JSON itself is
    valid.  ``raw_decode`` lets us consume the first complete object safely.
    """
    cleaned = text.lstrip("\ufeff \t\r\n")
    start = cleaned.find("{")
    if start < 0:
        raise json.JSONDecodeError("No JSON object found", cleaned, 0)
    obj, _end = json.JSONDecoder().raw_decode(cleaned[start:])
    if not isinstance(obj, dict):
        raise ValueError("Expected a JSON object from GDAL.")
    return obj


def verify_qgis(config: Config, tools: dict[str, Path]) -> str:
    qp = tools["qgis_process"]
    rc, text = _run_capture(command_for(qp, ["--version"]))
    if rc != 0:
        raise RastaError("QGIS version check failed.\n\n" + text[-2000:])
    if config.expected_qgis_version and config.expected_qgis_version not in text:
        raise RastaError(
            f"Rasta Pyramid Factory expects QGIS {config.expected_qgis_version}, but QGIS reported:\n\n{text.strip()}"
        )
    return next((line.strip() for line in text.splitlines() if line.strip()), text.strip())


def inspect_raster(config: Config, path: Path) -> RasterInfo:
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    tools = find_tools(config)
    rc, stdout, stderr = _run_capture_split([str(tools["gdalinfo"]), "-json", str(path)], timeout=120)
    if rc != 0:
        diagnostic = (stdout + "\n" + stderr).strip()
        raise RastaError("QGIS/GDAL could not inspect this raster.\n\n" + diagnostic[-3000:])
    try:
        # Parse stdout only. GDAL/codec warnings belong on stderr and must not be
        # appended to the machine-readable JSON stream. raw_decode also tolerates
        # harmless text which some builds append after the JSON object.
        data = _parse_json_payload(stdout)
        size = data["size"]
        width, height = int(size[0]), int(size[1])
    except Exception as exc:
        detail = stderr.strip()
        suffix = f"\n\nGDAL diagnostics:\n{detail[-1500:]}" if detail else ""
        raise RastaError(f"Could not read raster dimensions from GDAL: {exc}{suffix}") from exc
    cs = data.get("coordinateSystem") or {}
    wkt = str(cs.get("wkt") or "").strip()
    gt = data.get("geoTransform")
    has_crs = bool(wkt)
    has_gt = isinstance(gt, list) and len(gt) == 6
    driver = str((data.get("driverShortName") or data.get("driverLongName") or "Raster"))
    suggested = "geo" if has_crs and has_gt else "flat"
    return RasterInfo(path, width, height, driver, has_crs, has_gt, suggested)


def web_mercator_from_lonlat(lon: float, lat: float) -> tuple[float, float]:
    """Convert WGS84 lon/lat to EPSG:3857 meters for synthetic parking."""
    lat = max(-85.05112878, min(85.05112878, float(lat)))
    x = WEB_MERCATOR_HALF * float(lon) / 180.0
    y = WEB_MERCATOR_HALF * math.log(math.tan((90.0 + lat) * math.pi / 360.0)) / math.pi
    return x, y


def synthetic_bounds(
    width: int,
    height: int,
    meters_per_pixel: float = 1.0,
    center_x: float = 0.0,
    center_y: float = 0.0,
) -> tuple[float, float, float, float]:
    if width <= 0 or height <= 0 or meters_per_pixel <= 0:
        raise ValueError("Raster dimensions and synthetic scale must be positive.")
    half_w = width * meters_per_pixel / 2.0
    half_h = height * meters_per_pixel / 2.0
    return center_x - half_w, center_x + half_w, center_y - half_h, center_y + half_h


def synthetic_bounds_for_config(
    config: Config, width: int, height: int, meters_per_pixel: float | None = None
) -> tuple[float, float, float, float]:
    mpp = config.synthetic_meters_per_pixel if meters_per_pixel is None else float(meters_per_pixel)
    cx, cy = web_mercator_from_lonlat(config.synthetic_anchor_lon, config.synthetic_anchor_lat)
    return synthetic_bounds(width, height, mpp, cx, cy)


def recommended_max_zoom(meters_per_pixel: float) -> int:
    if meters_per_pixel <= 0:
        return 18
    return max(0, min(25, int(math.ceil(math.log2(WEB_MERCATOR_RES_Z0 / meters_per_pixel)))))


def _tile_xy_from_meters(x: float, y: float, z: int) -> tuple[int, int]:
    n = 1 << z
    world = WEB_MERCATOR_HALF * 2.0
    tx = int(math.floor(((x + WEB_MERCATOR_HALF) / world) * n))
    ty = int(math.floor(((WEB_MERCATOR_HALF - y) / world) * n))
    return max(0, min(n - 1, tx)), max(0, min(n - 1, ty))


def estimate_synthetic_tiles(bounds: tuple[float, float, float, float], zmin: int, zmax: int) -> int:
    xmin, xmax, ymin, ymax = bounds
    total = 0
    eps = 1e-9
    for z in range(zmin, zmax + 1):
        x0, y0 = _tile_xy_from_meters(xmin, ymax, z)
        x1, y1 = _tile_xy_from_meters(xmax - eps, ymin + eps, z)
        total += (x1 - x0 + 1) * (y1 - y0 + 1)
    return total


def _run_long_command(cmd: list[str], cancel_event, timeout: int | None = None) -> str:
    """Run a potentially long GDAL command with cancellation and captured diagnostics."""
    flags, si = _hidden_flags(new_group=True)
    with tempfile.TemporaryFile(mode="w+t", encoding="utf-8", errors="replace") as log:
        proc = subprocess.Popen(
            cmd, stdout=log, stderr=subprocess.STDOUT,
            creationflags=flags, startupinfo=si,
        )
        started = time.monotonic()
        while proc.poll() is None:
            if cancel_event is not None and cancel_event.is_set():
                terminate_tree(proc)
                raise BuildCancelled("Build cancelled by operator.")
            if timeout is not None and time.monotonic() - started > timeout:
                terminate_tree(proc)
                raise RastaError(f"Command timed out after {timeout} seconds: {cmd[0]}")
            time.sleep(0.20)
        rc = proc.wait()
        log.seek(0)
        text = log.read()
    if rc != 0:
        raise RastaError("External raster-preparation command failed.\n\n" + text[-4000:])
    return text


def overview_factors(width: int, height: int, target_max_dimension: int = 256) -> list[int]:
    """Return power-of-two overview factors down to a compact whole-image overview."""
    factors: list[int] = []
    factor = 2
    longest = max(int(width), int(height))
    while longest / factor > target_max_dimension:
        factors.append(factor)
        factor *= 2
    factors.append(factor)
    return factors


def make_synthetic_staged_geotiff(
    config: Config,
    tools: dict[str, Path],
    source: Path,
    staged_tif: Path,
    meters_per_pixel: float,
    emit,
    cancel_event,
) -> tuple[float, float, float, float]:
    """Decode a flat source once into a tiled, georeferenced working GeoTIFF.

    Giant PNG/JPEG images are stream-compressed and can be catastrophically slow
    when QGIS asks for thousands of small random windows.  Rasta therefore pays
    one sequential decode cost, writes a tiled BigTIFF working raster, and builds
    internal overview levels before QGIS starts the pyramid render.

    The source image is never modified and the staged TIFF is temporary.
    """
    info = inspect_raster(config, source)
    xmin, xmax, ymin, ymax = synthetic_bounds_for_config(config, info.width, info.height, meters_per_pixel)

    emit("stage", "Preparing optimized tiled working raster — decoding source once...", 0.04)
    cmd = [
        str(tools["gdal_translate"]),
        "-of", "GTiff",
        "-a_srs", "EPSG:3857",
        "-a_ullr", f"{xmin:.12f}", f"{ymax:.12f}", f"{xmax:.12f}", f"{ymin:.12f}",
        "-co", "TILED=YES",
        "-co", "BLOCKXSIZE=512",
        "-co", "BLOCKYSIZE=512",
        "-co", "BIGTIFF=IF_SAFER",
        # Temporary staging favors fast random access over storage efficiency.
        "-co", "COMPRESS=NONE",
        str(source), str(staged_tif),
    ]
    _run_long_command(cmd, cancel_event=cancel_event)
    if not staged_tif.is_file() or staged_tif.stat().st_size <= 0:
        raise RastaError("GDAL did not create the optimized working GeoTIFF.")

    factors = overview_factors(info.width, info.height)
    emit(
        "overview",
        "Building working overviews for fast QGIS random access — " + ", ".join(map(str, factors)),
        0.10,
    )
    addo = [
        str(tools["gdaladdo"]),
        "-r", "average",
        "--config", "COMPRESS_OVERVIEW", "DEFLATE",
        "--config", "ZLEVEL_OVERVIEW", "1",
        "--config", "BIGTIFF_OVERVIEW", "YES",
        str(staged_tif),
        *[str(f) for f in factors],
    ]
    _run_long_command(addo, cancel_event=cancel_event)
    return xmin, xmax, ymin, ymax

def inspect_mbtiles(path: Path) -> dict:
    uri = path.resolve().as_uri() + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    try:
        cols = {row[1] for row in con.execute("PRAGMA table_info(tiles)")}
        if not {"zoom_level", "tile_column", "tile_row", "tile_data"}.issubset(cols):
            raise RastaError("MBTiles does not expose the standard raster tiles table.")
        row = con.execute("SELECT MIN(zoom_level), MAX(zoom_level), COUNT(*) FROM tiles").fetchone()
        if not row or row[0] is None or int(row[2]) <= 0:
            raise RastaError("MBTiles contains no tiles.")
        md = dict(con.execute("SELECT name,value FROM metadata"))
        fmt = (md.get("format") or "").lower()
        if fmt not in {"png", "jpg", "jpeg"}:
            raise RastaError(f"Unexpected raster tile format: {fmt!r}")
        return {"min_zoom": int(row[0]), "max_zoom": int(row[1]), "tile_count": int(row[2]), "metadata": md}
    finally:
        con.close()


def inspect_tpkx(path: Path) -> dict:
    if not path.is_file() or path.stat().st_size <= 0:
        raise RastaError("TPKX output is missing or empty.")
    with zipfile.ZipFile(path, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise RastaError(f"TPKX ZIP verification failed at {bad}")
        names = set(zf.namelist())
        for required in {"root.json", "iteminfo.json", "thumbnail.png"}:
            if required not in names:
                raise RastaError(f"TPKX is missing {required}")
        bundles = [n for n in names if n.lower().endswith(".bundle")]
        if not bundles:
            raise RastaError("TPKX contains no Compact Cache V2 bundles.")
        root = json.loads(zf.read("root.json").decode("utf-8"))
    if (root.get("storageInfo") or {}).get("storageFormat") != "esriMapCacheStorageModeCompactV2":
        raise RastaError("TPKX does not identify Compact Cache V2 storage.")
    return {"bundle_count": len(bundles), "min_zoom": int(root.get("minLOD", -1)), "max_zoom": int(root.get("maxLOD", -1))}


def _console_python() -> str:
    exe = Path(sys.executable)
    if exe.name.lower() in {"pythonw.exe", "pythonw"}:
        c = exe.with_name("python.exe" if exe.suffix.lower() == ".exe" else "python")
        if c.is_file():
            return str(c)
    return str(exe)


def _run_converter(converter: Path, mbtiles: Path, tpkx: Path, emit, cancel_event):
    flags, si = _hidden_flags(new_group=True)
    proc = subprocess.Popen(
        [_console_python(), "-u", str(converter), str(mbtiles), str(tpkx)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        encoding="utf-8", errors="replace", bufsize=1,
        creationflags=flags, startupinfo=si, cwd=str(converter.parent),
    )
    tail = []
    assert proc.stdout is not None
    try:
        for raw in iter(proc.stdout.readline, ""):
            line = raw.rstrip()
            if line:
                tail.append(line); tail = tail[-30:]
                if line.startswith("Tiles "):
                    emit("convert", "TPKX conversion — " + line, None)
                elif line.startswith("Packaging "):
                    emit("package", line, None)
            if cancel_event is not None and cancel_event.is_set():
                terminate_tree(proc)
                raise BuildCancelled("Build cancelled by operator.")
        rc = proc.wait()
    finally:
        try: proc.stdout.close()
        except Exception: pass
    if rc != 0:
        raise RastaError("TPKX converter failed.\n\n" + "\n".join(tail[-15:]))


def _publish(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        raise FileExistsError(f"Output already exists: {dst}")
    partial = dst.with_name("." + dst.name + ".__publishing")
    if partial.exists():
        partial.unlink()
    shutil.copy2(src, partial)
    partial.replace(dst)


def _run_qgis_worker(config: Config, tools: dict[str, Path], worker: Path, job: dict, jobfile: Path, emit, cancel_event):
    jobfile.write_text(json.dumps(job, indent=2), encoding="utf-8")
    bat = tools["python_qgis"]
    flags, si = _hidden_flags(new_group=True)
    env = os.environ.copy()
    env.setdefault("QT_QPA_PLATFORM", "offscreen")
    proc = subprocess.Popen(
        command_for(bat, [str(worker), str(jobfile)]),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
        encoding="utf-8", errors="replace", bufsize=1,
        creationflags=flags, startupinfo=si, env=env,
    )
    assert proc.stdout is not None
    tail = []
    result = None
    try:
        while True:
            if cancel_event is not None and cancel_event.is_set():
                terminate_tree(proc)
                raise BuildCancelled("Build cancelled by operator.")
            line = proc.stdout.readline()
            if line == "" and proc.poll() is not None:
                break
            line = line.rstrip("\r\n")
            if not line:
                continue
            tail.append(line); tail = tail[-40:]
            if line.startswith("RPF_PROGRESS "):
                try:
                    pct = float(line.split()[1])
                    emit("qgis", f"QGIS is building the raster pyramid — {pct:.1f}%", 0.16 + max(0.0, min(0.72, pct/100*0.72)))
                except Exception:
                    pass
            elif line.startswith("RPF_INFO "):
                emit("qgis", line[9:], None)
            elif line.startswith("RPF_RESULT_JSON "):
                try: result = json.loads(line[len("RPF_RESULT_JSON "):])
                except Exception: pass
        rc = proc.wait()
    finally:
        try: proc.stdout.close()
        except Exception: pass
    if rc != 0:
        raise RastaError("Headless QGIS worker failed.\n\n" + "\n".join(tail[-20:]))
    if result is None:
        raise RastaError("QGIS worker completed without returning a result record.")
    return result


def build(
    config: Config,
    input_file: Path,
    raster_mode: str,
    output_mode: str,
    output_dir: Path,
    output_stem: str,
    zoom_min: int,
    zoom_max: int,
    meters_per_pixel: float = 1.0,
    progress: Optional[ProgressCallback] = None,
    cancel_event: Optional[threading.Event] = None,
) -> BuildResult:
    input_file = Path(input_file).expanduser().resolve()
    output_dir = Path(output_dir).expanduser().resolve()
    if not input_file.is_file():
        raise FileNotFoundError(input_file)
    if qgis_desktop_running():
        raise RastaError("QGIS Desktop is running. Close QGIS Desktop before building.")
    if not (0 <= zoom_min <= zoom_max <= 25):
        raise ValueError("Zooms must satisfy 0 <= minimum <= maximum <= 25.")
    output_mode = output_mode.lower()
    if output_mode not in {"mbtiles", "tpkx", "both"}:
        raise ValueError("Output mode must be MBTiles, TPKX, or Both.")
    output_stem = re.sub(r'[<>:"/\\|?*]+', "_", output_stem.strip()).strip(" .") or input_file.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    final_mb = output_dir / f"{output_stem}.mbtiles"
    final_tpkx = output_dir / f"{output_stem}.tpkx"
    if output_mode in {"mbtiles", "both"} and final_mb.exists():
        raise FileExistsError(final_mb)
    if output_mode in {"tpkx", "both"} and final_tpkx.exists():
        raise FileExistsError(final_tpkx)

    def emit(stage, msg, frac=None):
        if progress: progress(stage, msg, frac)

    tools = find_tools(config)
    emit("preflight", "Verifying QGIS installation...", 0.01)
    verify_qgis(config, tools)
    info = inspect_raster(config, input_file)
    mode = raster_mode.lower()
    if mode == "auto": mode = info.mode_suggested
    if mode not in {"flat", "geo"}:
        raise ValueError("Raster mode must be Auto, Flat, or Geo.")
    if mode == "geo" and not (info.has_crs and info.has_geotransform):
        raise RastaError("GEO RASTER mode requires a raster with a valid CRS and geotransform.")

    work = Path(tempfile.mkdtemp(prefix="Rasta_Pyramid_"))
    started = time.monotonic()
    temp_mb = work / "raster_pyramid.mbtiles"
    temp_tpkx = work / "raster_pyramid.tpkx"
    worker = config.base_dir / "RPF_QGIS_WORKER.py"
    converter = config.base_dir / "MBTiles_to_TPKX_v0_1_0.py"
    try:
        source_for_qgis = input_file
        if mode == "flat":
            staged_tif = work / "rasta_working_raster.tif"
            make_synthetic_staged_geotiff(
                config, tools, input_file, staged_tif, meters_per_pixel, emit, cancel_event
            )
            source_for_qgis = staged_tif
        job = {
            "input": str(source_for_qgis),
            "layer_name": input_file.stem,
            "output_mbtiles": str(temp_mb),
            "zoom_min": zoom_min,
            "zoom_max": zoom_max,
            "dpi": config.dpi,
            "antialias": config.antialias,
            "tile_format": config.tile_format,
            "quality": config.quality,
            "metatile_size": config.metatile_size,
            "project_crs": "EPSG:3857",
        }
        emit("qgis", "Starting headless QGIS pyramid engine against optimized working raster...", 0.16)
        _run_qgis_worker(config, tools, worker, job, work / "job.json", emit, cancel_event)
        if not temp_mb.is_file():
            raise RastaError("QGIS did not create the MBTiles output.")
        emit("verify_mb", "Verifying MBTiles pyramid...", 0.90)
        mb_info = inspect_mbtiles(temp_mb)

        published_mb = None
        published_tpkx = None
        bundle_count = 0
        if output_mode in {"mbtiles", "both"}:
            emit("publish_mb", "Publishing verified MBTiles...", 0.93)
            _publish(temp_mb, final_mb)
            inspect_mbtiles(final_mb)
            published_mb = final_mb

        if output_mode in {"tpkx", "both"}:
            if not converter.is_file():
                raise RastaError(f"Frozen TPKX converter is missing: {converter}")
            emit("convert", "Converting raster pyramid to native TPKX...", 0.94)
            _run_converter(converter, temp_mb, temp_tpkx, emit, cancel_event)
            emit("verify_tpkx", "Verifying Compact Cache V2 TPKX...", 0.98)
            tinfo = inspect_tpkx(temp_tpkx)
            bundle_count = int(tinfo["bundle_count"])
            _publish(temp_tpkx, final_tpkx)
            inspect_tpkx(final_tpkx)
            published_tpkx = final_tpkx

        elapsed = time.monotonic() - started
        emit("complete", "COMPLETE — pyramid products verified and published.", 1.0)
        return BuildResult(
            input_file=input_file, mode=mode, output_mode=output_mode,
            mbtiles_file=published_mb, tpkx_file=published_tpkx,
            tile_count=int(mb_info["tile_count"]), min_zoom=int(mb_info["min_zoom"]),
            max_zoom=int(mb_info["max_zoom"]), bundle_count=bundle_count,
            elapsed_seconds=elapsed,
        )
    finally:
        shutil.rmtree(work, ignore_errors=True)
