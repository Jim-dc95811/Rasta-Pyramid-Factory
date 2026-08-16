#!/usr/bin/env python3
"""
MBTiles -> ArcGIS TPKX converter

Purpose:
    Convert raster MBTiles (PNG or JPEG, Web Mercator/TMS scheme) into an
    Esri Compact Tile Package (.tpkx) using the published Tile Package
    Specification and Compact Cache V2 bundle format.

Dependencies:
    Python 3 standard library only.

Notes:
    - MBTiles tile_row is TMS (bottom-origin). ArcGIS compact cache rows are
      top-origin, so Y is flipped during conversion.
    - TPKX is the current, published Esri tile-package format. This script does
      not create legacy .tpk (Compact Cache V1).
    - For large datasets, temporary working data plus the final TPKX can require
      roughly twice the source MBTiles size in free disk space.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import shutil
import sqlite3
import struct
import sys
import time
import uuid
import zipfile
import zlib
import binascii

PACKET_SIZE = 128
TILES_PER_BUNDLE = PACKET_SIZE * PACKET_SIZE
INDEX_SIZE = TILES_PER_BUNDLE * 8
FIXED_BUNDLE_SIZE = 64 + INDEX_SIZE
WEB_MERCATOR_HALF_WORLD = 20037508.342789244
WEB_MERCATOR_ORIGIN_X = -20037508.342787001
WEB_MERCATOR_ORIGIN_Y = 20037508.342787001
BASE_RESOLUTION = 156543.03392804097
DPI = 96
INCHES_PER_METER = 39.37
MAX_WEB_MERCATOR_LAT = 85.0511287798066


class ConversionError(RuntimeError):
    pass


def fmt_int(n: int) -> str:
    return f"{n:,}"


def format_elapsed(seconds: float) -> str:
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def read_metadata(conn: sqlite3.Connection) -> dict[str, str]:
    try:
        rows = conn.execute("SELECT name, value FROM metadata").fetchall()
    except sqlite3.Error as exc:
        raise ConversionError(f"Could not read MBTiles metadata table: {exc}") from exc
    return {str(k): str(v) for k, v in rows}


def validate_mbtiles(conn: sqlite3.Connection) -> tuple[int, int, int]:
    try:
        cols = [row[1] for row in conn.execute("PRAGMA table_info(tiles)")]
    except sqlite3.Error as exc:
        raise ConversionError(f"Could not inspect MBTiles tiles table: {exc}") from exc

    needed = {"zoom_level", "tile_column", "tile_row", "tile_data"}
    if not needed.issubset(cols):
        raise ConversionError(
            "Input does not expose a standard MBTiles tiles table with "
            "zoom_level, tile_column, tile_row, and tile_data."
        )

    row = conn.execute(
        "SELECT MIN(zoom_level), MAX(zoom_level), COUNT(*) FROM tiles"
    ).fetchone()
    if not row or row[0] is None:
        raise ConversionError("MBTiles contains no tiles.")

    min_zoom, max_zoom, count = int(row[0]), int(row[1]), int(row[2])
    if min_zoom < 0 or max_zoom > 30:
        raise ConversionError(f"Unexpected zoom range {min_zoom}-{max_zoom}.")
    return min_zoom, max_zoom, count


def detect_tile_format(metadata: dict[str, str], sample: bytes) -> str:
    declared = metadata.get("format", "").strip().lower()
    if declared in {"png", "image/png"}:
        return "PNG"
    if declared in {"jpg", "jpeg", "image/jpeg"}:
        return "JPEG"
    if declared in {"pbf", "mvt", "webp", "image/webp"}:
        raise ConversionError(
            f"Unsupported MBTiles tile format '{declared}'. This converter is for raster PNG/JPEG tiles."
        )

    if sample.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if sample.startswith(b"\xff\xd8\xff"):
        return "JPEG"
    raise ConversionError(
        "Could not identify raster tile format. Only PNG and JPEG MBTiles are supported."
    )


def validate_png_tile_size(sample: bytes) -> None:
    if not sample.startswith(b"\x89PNG\r\n\x1a\n") or len(sample) < 24:
        return
    width, height = struct.unpack(">II", sample[16:24])
    if width != 256 or height != 256:
        raise ConversionError(
            f"This first version expects 256x256 tiles; input PNG is {width}x{height}."
        )


def clamp_lat(lat: float) -> float:
    return max(-MAX_WEB_MERCATOR_LAT, min(MAX_WEB_MERCATOR_LAT, lat))


def lonlat_to_mercator(lon: float, lat: float) -> tuple[float, float]:
    lat = clamp_lat(lat)
    x = WEB_MERCATOR_HALF_WORLD * lon / 180.0
    y = WEB_MERCATOR_HALF_WORLD * math.log(
        math.tan((90.0 + lat) * math.pi / 360.0)
    ) / math.pi
    return x, y


def xyz_tile_bounds_lonlat(z: int, x: int, y: int) -> tuple[float, float, float, float]:
    n = 2.0 ** z
    west = x / n * 360.0 - 180.0
    east = (x + 1) / n * 360.0 - 180.0

    def tile_y_to_lat(tile_y: float) -> float:
        merc_n = math.pi - (2.0 * math.pi * tile_y / n)
        return math.degrees(math.atan(math.sinh(merc_n)))

    north = tile_y_to_lat(y)
    south = tile_y_to_lat(y + 1)
    return west, south, east, north


def derive_bounds(conn: sqlite3.Connection, metadata: dict[str, str]) -> tuple[float, float, float, float]:
    bounds = metadata.get("bounds", "").strip()
    if bounds:
        try:
            west, south, east, north = [float(v.strip()) for v in bounds.split(",")]
            if west < east and south < north:
                return west, south, east, north
        except Exception:
            pass

    # Fallback: union tile envelopes across every represented zoom level.
    west = 180.0
    south = 90.0
    east = -180.0
    north = -90.0

    rows = conn.execute(
        "SELECT zoom_level, MIN(tile_column), MAX(tile_column), MIN(tile_row), MAX(tile_row) "
        "FROM tiles GROUP BY zoom_level"
    )
    found = False
    for z, min_x, max_x, min_tms_y, max_tms_y in rows:
        z = int(z)
        n = 1 << z
        min_xyz_y = n - 1 - int(max_tms_y)
        max_xyz_y = n - 1 - int(min_tms_y)
        a = xyz_tile_bounds_lonlat(z, int(min_x), min_xyz_y)
        b = xyz_tile_bounds_lonlat(z, int(max_x), max_xyz_y)
        west = min(west, a[0])
        north = max(north, a[3])
        east = max(east, b[2])
        south = min(south, b[1])
        found = True

    if not found:
        raise ConversionError("Unable to derive geographic bounds from MBTiles.")
    return west, south, east, north


def make_spatial_reference() -> dict:
    return {
        "wkid": 102100,
        "latestWkid": 3857,
    }


def lod_table(max_level: int = 23) -> list[dict]:
    lods = []
    for z in range(max_level + 1):
        resolution = BASE_RESOLUTION / (2 ** z)
        scale = resolution * DPI * INCHES_PER_METER
        lods.append({"level": z, "resolution": resolution, "scale": scale})
    return lods


def make_root_json(
    name: str,
    tile_format: str,
    min_zoom: int,
    max_zoom: int,
    bounds_lonlat: tuple[float, float, float, float],
) -> dict:
    west, south, east, north = bounds_lonlat
    xmin, ymin = lonlat_to_mercator(west, south)
    xmax, ymax = lonlat_to_mercator(east, north)
    sr = make_spatial_reference()
    lods = lod_table(max(23, max_zoom))

    extent = {
        "xmin": xmin,
        "ymin": ymin,
        "xmax": xmax,
        "ymax": ymax,
        "spatialReference": sr,
    }

    return {
        "tileImageInfo": {
            "format": tile_format,
            "compressionQuality": 0 if tile_format == "PNG" else 90,
        },
        "name": name,
        "version": 1.0,
        "serviceDescription": "Converted from MBTiles",
        "tileBundlesPath": "./tile",
        "spatialReference": sr,
        "units": "esriMeters",
        "minLOD": min_zoom,
        "maxLOD": max_zoom,
        "minScale": lods[min_zoom]["scale"],
        "maxScale": lods[max_zoom]["scale"],
        "resampling": True,
        "tileInfo": {
            "rows": 256,
            "cols": 256,
            "dpi": DPI,
            "origin": {"x": WEB_MERCATOR_ORIGIN_X, "y": WEB_MERCATOR_ORIGIN_Y},
            "spatialReference": sr,
            "lods": lods,
        },
        "exportTilesAllowed": False,
        "storageInfo": {
            "storageFormat": "esriMapCacheStorageModeCompactV2",
            "packetSize": PACKET_SIZE,
        },
        "initialExtent": extent,
        "fullExtent": extent,
    }


def make_iteminfo_json(
    name: str,
    bounds_lonlat: tuple[float, float, float, float],
    metadata: dict[str, str],
) -> dict:
    west, south, east, north = bounds_lonlat
    description = metadata.get("description", "")
    attribution = metadata.get("attribution", "")
    if attribution:
        description = (description + "\n" if description else "") + attribution

    return {
        "creator": "MBTiles_to_TPKX",
        "name": name,
        "guid": str(uuid.uuid4()).upper(),
        "version": 1.0,
        "created": int(time.time() * 1000),
        "snippet": "Converted from MBTiles",
        "description": description,
        "summary": "Raster tile package converted from MBTiles",
        "title": name,
        "tags": ["MBTiles", "TPKX"],
        "type": "Compact Tile Package",
        "typeKeywords": ["Compact Tile Package", "Tile Package", "tpkx"],
        "thumbnail": "./thumbnail.png",
        "extent": {
            "xmin": west,
            "ymin": south,
            "xmax": east,
            "ymax": north,
            "spatialReference": {"wkid": 4326, "latestWkid": 4326},
        },
    }


def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    body = chunk_type + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", binascii.crc32(body) & 0xFFFFFFFF)


def write_placeholder_thumbnail(path: Path, width: int = 200, height: int = 133) -> None:
    # 24-bit RGB PNG, neutral dark gray. No third-party imaging library required.
    row = b"\x00" + (b"\x34\x34\x34" * width)
    raw = row * height
    png = b"\x89PNG\r\n\x1a\n"
    png += png_chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
    png += png_chunk(b"IDAT", zlib.compress(raw, 9))
    png += png_chunk(b"IEND", b"")
    path.write_bytes(png)


class BundleWriter:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fd = path.open("w+b")
        self.index = [0] * TILES_PER_BUNDLE
        self.max_tile_size = 0
        self.offset = FIXED_BUNDLE_SIZE
        self._write_empty_header_and_index()

    def _write_empty_header_and_index(self) -> None:
        header = struct.pack(
            "<4I3Q6I",
            3,                  # Version
            TILES_PER_BUNDLE,   # Record Count
            0,                  # Maximum Tile Size (updated on close)
            5,                  # Offset Byte Count
            0,                  # Slack Space
            FIXED_BUNDLE_SIZE,  # File Size (updated on close)
            40,                 # User Header Offset
            20 + INDEX_SIZE,    # User Header Size
            3,                  # Legacy
            16,                 # Legacy
            TILES_PER_BUNDLE,   # Legacy
            5,                  # Legacy
            INDEX_SIZE,         # Index Size
        )
        self.fd.write(header)
        self.fd.write(b"\x00" * INDEX_SIZE)

    def add_tile(self, row: int, col: int, tile_data: bytes) -> None:
        tile_size = len(tile_data)
        if tile_size >= (1 << 24):
            raise ConversionError(f"Tile is too large for Compact Cache V2: {tile_size} bytes")

        self.fd.seek(0, os.SEEK_END)
        self.fd.write(struct.pack("<I", tile_size))
        tile_offset = self.fd.tell()
        self.fd.write(tile_data)

        index_pos = (row % PACKET_SIZE) * PACKET_SIZE + (col % PACKET_SIZE)
        self.index[index_pos] = tile_offset + (tile_size << 40)
        self.max_tile_size = max(self.max_tile_size, tile_size)
        self.offset = self.fd.tell()

    def close(self) -> None:
        if self.fd.closed:
            return
        self.fd.seek(8)
        self.fd.write(struct.pack("<I", self.max_tile_size))
        self.fd.seek(24)
        self.fd.write(struct.pack("<Q", self.offset))
        self.fd.seek(64)
        self.fd.write(struct.pack(f"<{TILES_PER_BUNDLE}Q", *self.index))
        self.fd.flush()
        self.fd.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()


def bundle_name(row: int, col: int) -> str:
    start_row = (row // PACKET_SIZE) * PACKET_SIZE
    start_col = (col // PACKET_SIZE) * PACKET_SIZE
    return f"R{start_row:04x}C{start_col:04x}.bundle"


def build_bundles(
    conn: sqlite3.Connection,
    work_root: Path,
    tile_count: int,
    progress_every: int = 5000,
) -> int:
    tile_root = work_root / "tile"
    tile_root.mkdir(parents=True, exist_ok=True)

    # MBTiles rows are TMS. Sort in resulting ArcGIS bundle order so only one
    # bundle needs to be open at a time.
    query = """
        SELECT zoom_level, tile_column, tile_row, tile_data
        FROM tiles
        ORDER BY
            zoom_level,
            (((1 << zoom_level) - 1 - tile_row) / 128),
            (tile_column / 128),
            ((1 << zoom_level) - 1 - tile_row),
            tile_column
    """

    current_key = None
    current_bundle = None
    processed = 0
    bundle_count = 0
    started = time.monotonic()

    try:
        for z, x, tms_y, tile_data in conn.execute(query):
            z = int(z)
            x = int(x)
            tms_y = int(tms_y)
            y = (1 << z) - 1 - tms_y

            b_row = (y // PACKET_SIZE) * PACKET_SIZE
            b_col = (x // PACKET_SIZE) * PACKET_SIZE
            key = (z, b_row, b_col)

            if key != current_key:
                if current_bundle is not None:
                    current_bundle.close()
                level_dir = tile_root / f"L{z:02d}"
                level_dir.mkdir(parents=True, exist_ok=True)
                current_bundle = BundleWriter(level_dir / bundle_name(y, x))
                current_key = key
                bundle_count += 1

            current_bundle.add_tile(y, x, bytes(tile_data))
            processed += 1

            if processed == 1 or processed % progress_every == 0 or processed == tile_count:
                pct = (processed / tile_count * 100.0) if tile_count else 100.0
                print(
                    f"Tiles {fmt_int(processed)} / {fmt_int(tile_count)} "
                    f"({pct:6.2f}%)  Bundles {fmt_int(bundle_count)}  "
                    f"Elapsed {format_elapsed(time.monotonic() - started)}",
                    flush=True,
                )
    finally:
        if current_bundle is not None:
            current_bundle.close()

    return bundle_count


def package_tpkx(work_root: Path, output_path: Path) -> None:
    if output_path.exists():
        output_path.unlink()

    files = [p for p in work_root.rglob("*") if p.is_file()]
    files.sort(key=lambda p: str(p.relative_to(work_root)).lower())

    print(f"Packaging {fmt_int(len(files))} files into {output_path.name} ...", flush=True)
    with zipfile.ZipFile(
        output_path,
        "w",
        compression=zipfile.ZIP_STORED,
        allowZip64=True,
    ) as zf:
        for path in files:
            arcname = path.relative_to(work_root).as_posix()
            zf.write(path, arcname)

    with zipfile.ZipFile(output_path, "r") as zf:
        bad = zf.testzip()
        if bad is not None:
            raise ConversionError(f"TPKX ZIP verification failed at entry: {bad}")
        names = set(zf.namelist())
        for required in {"root.json", "iteminfo.json", "thumbnail.png"}:
            if required not in names:
                raise ConversionError(f"TPKX verification failed: missing {required}")


def convert_mbtiles_to_tpkx(input_path: Path, output_path: Path, keep_work: bool = False) -> None:
    input_path = input_path.resolve()
    output_path = output_path.resolve()

    if not input_path.is_file():
        raise ConversionError(f"Input file not found: {input_path}")
    if input_path == output_path:
        raise ConversionError("Input and output paths must be different.")
    if output_path.suffix.lower() != ".tpkx":
        output_path = output_path.with_suffix(".tpkx")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    work_root = output_path.parent / f".{output_path.stem}_tpkx_work"

    if work_root.exists():
        shutil.rmtree(work_root)
    work_root.mkdir(parents=True)

    started = time.monotonic()
    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print(f"Work  : {work_root}")

    try:
        # Read-only URI avoids accidental writes to the source MBTiles.
        uri = input_path.as_uri() + "?mode=ro"
        conn = sqlite3.connect(uri, uri=True)
        try:
            metadata = read_metadata(conn)
            min_zoom, max_zoom, tile_count = validate_mbtiles(conn)
            sample_row = conn.execute("SELECT tile_data FROM tiles LIMIT 1").fetchone()
            if not sample_row:
                raise ConversionError("MBTiles contains no tile data.")
            sample = bytes(sample_row[0])
            tile_format = detect_tile_format(metadata, sample)
            if tile_format == "PNG":
                validate_png_tile_size(sample)

            name = metadata.get("name", "").strip() or input_path.stem
            bounds = derive_bounds(conn, metadata)

            print(f"Name  : {name}")
            print(f"Format: {tile_format}")
            print(f"Zooms : {min_zoom}-{max_zoom}")
            print(f"Tiles : {fmt_int(tile_count)}")
            print(
                "Bounds: "
                f"{bounds[0]:.8f}, {bounds[1]:.8f}, {bounds[2]:.8f}, {bounds[3]:.8f}"
            )
            print()

            root_json = make_root_json(name, tile_format, min_zoom, max_zoom, bounds)
            iteminfo_json = make_iteminfo_json(name, bounds, metadata)
            (work_root / "root.json").write_text(
                json.dumps(root_json, ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
            (work_root / "iteminfo.json").write_text(
                json.dumps(iteminfo_json, ensure_ascii=False, separators=(",", ":")),
                encoding="utf-8",
            )
            write_placeholder_thumbnail(work_root / "thumbnail.png")

            bundle_count = build_bundles(conn, work_root, tile_count)
        finally:
            conn.close()

        package_tpkx(work_root, output_path)

        elapsed = time.monotonic() - started
        print()
        print("CONVERSION COMPLETE")
        print(f"Tiles   : {fmt_int(tile_count)}")
        print(f"Bundles : {fmt_int(bundle_count)}")
        print(f"Output  : {output_path}")
        print(f"Bytes   : {fmt_int(output_path.stat().st_size)}")
        print(f"Elapsed : {format_elapsed(elapsed)}")

    except Exception:
        print()
        print(f"Working files preserved at: {work_root}", file=sys.stderr)
        raise
    else:
        if keep_work:
            print(f"Working cache preserved at: {work_root}")
        else:
            shutil.rmtree(work_root, ignore_errors=True)


def choose_paths_gui() -> tuple[Path | None, Path | None]:
    try:
        import tkinter as tk
        from tkinter import filedialog
    except Exception:
        return None, None

    root = tk.Tk()
    root.withdraw()
    try:
        input_name = filedialog.askopenfilename(
            title="Select MBTiles file",
            filetypes=[("MBTiles", "*.mbtiles"), ("All files", "*.*")],
        )
        if not input_name:
            return None, None
        input_path = Path(input_name)

        output_name = filedialog.asksaveasfilename(
            title="Save ArcGIS Tile Package",
            defaultextension=".tpkx",
            initialfile=input_path.stem + ".tpkx",
            filetypes=[("ArcGIS Compact Tile Package", "*.tpkx")],
        )
        if not output_name:
            return None, None
        return input_path, Path(output_name)
    finally:
        root.destroy()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert raster Web Mercator MBTiles to ArcGIS TPKX (Compact Cache V2)."
    )
    parser.add_argument("input", nargs="?", help="Input .mbtiles file")
    parser.add_argument("output", nargs="?", help="Output .tpkx file")
    parser.add_argument(
        "--keep-work",
        action="store_true",
        help="Keep the intermediate unpacked Compact Cache V2 folder.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.input:
        input_path = Path(args.input)
        output_path = Path(args.output) if args.output else input_path.with_suffix(".tpkx")
    else:
        input_path, output_path = choose_paths_gui()
        if input_path is None or output_path is None:
            print("Cancelled.")
            return 1

    try:
        convert_mbtiles_to_tpkx(input_path, output_path, keep_work=args.keep_work)
    except ConversionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("Cancelled by user.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"UNEXPECTED ERROR: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
