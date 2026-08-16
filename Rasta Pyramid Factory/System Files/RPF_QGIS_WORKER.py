#!/usr/bin/env python3
"""Runs inside QGIS's own Python environment. Do not launch directly."""
from __future__ import annotations
import json
from pathlib import Path
import os
import sys

if len(sys.argv) != 2:
    print("RPF_INFO Worker expects one JSON job file.")
    raise SystemExit(2)

job = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))

from qgis.core import (
    QgsApplication, QgsCoordinateReferenceSystem, QgsCoordinateTransform,
    QgsProcessingFeedback, QgsProject, QgsRasterLayer,
)

prefix = os.environ.get("QGIS_PREFIX_PATH")
if prefix:
    QgsApplication.setPrefixPath(prefix, True)
qgs = QgsApplication([], False)
qgs.initQgis()
try:
    # QGIS Processing is a core plugin; make sure its Python package is visible.
    plugin_path = Path(QgsApplication.pkgDataPath()) / "python" / "plugins"
    if plugin_path.is_dir() and str(plugin_path) not in sys.path:
        sys.path.insert(0, str(plugin_path))
    from processing.core.Processing import Processing
    Processing.initialize()
    from qgis.analysis import QgsNativeAlgorithms
    if not any(provider.id() == "native" for provider in QgsApplication.processingRegistry().providers()):
        QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
    import processing

    class Feedback(QgsProcessingFeedback):
        def __init__(self):
            super().__init__()
            self.last = -1
        def setProgress(self, progress):
            super().setProgress(progress)
            p = int(progress)
            if p != self.last:
                self.last = p
                print(f"RPF_PROGRESS {float(progress):.3f}", flush=True)
        def pushInfo(self, info):
            super().pushInfo(info)
            print("RPF_INFO " + str(info), flush=True)
        def pushWarning(self, warning):
            super().pushWarning(warning)
            print("RPF_INFO WARNING: " + str(warning), flush=True)

    project = QgsProject.instance()
    project.clear()
    target_crs = QgsCoordinateReferenceSystem(job.get("project_crs", "EPSG:3857"))
    if not target_crs.isValid():
        raise RuntimeError("Invalid target CRS.")
    project.setCrs(target_crs)

    layer = QgsRasterLayer(job["input"], job.get("layer_name", "Rasta Raster"))
    if not layer.isValid():
        raise RuntimeError("QGIS could not load the raster input.")
    if not layer.crs().isValid():
        raise RuntimeError("Raster has no valid CRS after preparation.")
    project.addMapLayer(layer)

    ext = layer.extent()
    if layer.crs() != target_crs:
        ct = QgsCoordinateTransform(layer.crs(), target_crs, project)
        ext = ct.transformBoundingBox(ext)
    extent_text = f"{ext.xMinimum():.12f},{ext.xMaximum():.12f},{ext.yMinimum():.12f},{ext.yMaximum():.12f} [EPSG:3857]"
    print("RPF_INFO Raster extent: " + extent_text, flush=True)

    params = {
        "EXTENT": extent_text,
        "ZOOM_MIN": int(job["zoom_min"]),
        "ZOOM_MAX": int(job["zoom_max"]),
        "DPI": int(job.get("dpi", 96)),
        "BACKGROUND_COLOR": "0,0,0,0",
        "ANTIALIAS": bool(job.get("antialias", True)),
        "TILE_FORMAT": int(job.get("tile_format", 0)),
        "QUALITY": int(job.get("quality", 75)),
        "METATILESIZE": int(job.get("metatile_size", 4)),
        "OUTPUT_FILE": job["output_mbtiles"],
    }
    feedback = Feedback()
    result = processing.run("native:tilesxyzmbtiles", params, feedback=feedback)
    out = Path(result.get("OUTPUT_FILE") or job["output_mbtiles"])
    if not out.is_file():
        raise RuntimeError("QGIS processing completed without an MBTiles file.")
    print("RPF_RESULT_JSON " + json.dumps({"output": str(out), "extent": extent_text}), flush=True)
finally:
    qgs.exitQgis()
