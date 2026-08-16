# Technical Architecture

## Design principle

Rasta separates three concerns:

1. **source raster** — the original pixels;
2. **QGIS manufacturing** — multiscale rendering into raster MBTiles;
3. **output container** — MBTiles directly or optional Compact Cache V2 / TPKX packaging.

```text
source raster
    ↓
GDAL inspection
    ↓
flat? ────────────────┐
    │                 │
    yes               no / valid georaster
    ↓                 ↓
one-time staging      preserve real CRS/geotransform
    ↓                 │
tiled working GeoTIFF │
    ↓                 │
internal overviews    │
    └───────┬─────────┘
            ↓
QGIS 3.44.9 headless worker
            ↓
native:tilesxyzmbtiles
            ↓
verified MBTiles
            ↓
optional frozen MBTiles_to_TPKX_v0_1_0.py
            ↓
verified TPKX
```

## Raster inspection

The normal Python GUI invokes the QGIS/GDAL installation's `gdalinfo -json`. Machine-readable JSON is read from stdout separately from diagnostic stderr; the parser deliberately tolerates harmless trailing diagnostic text.

The raster is automatically classified as a real georaster only when both a usable CRS and geotransform are present.

## Synthetic flat-image placement

Synthetic placement is not claimed to be real geography.

For width `W`, height `H`, and scale `S` projected meters/source-pixel:

```text
half_width  = (W × S) / 2
half_height = (H × S) / 2
xmin = center_x - half_width
xmax = center_x + half_width
ymin = center_y - half_height
ymax = center_y + half_height
```

v0.1.3 uses a deterministic WGS84 anchor of **30°N, 80°W**, converted internally to EPSG:3857 meters. This parks flat images in the Atlantic east of Florida rather than at the 0,0 longitude/latitude intersection off Africa.

The default scale remains **1 source pixel = 1 projected meter**. This makes the maximum useful Web Mercator zoom fall around Z17, with Z18 providing slight oversampling for visual inspection.

## Why flat PNG/JPEG inputs are staged

The first automated Montreal bench run exposed a performance defect in the original approach. Leaving QGIS to make thousands of small random reads directly from a giant stream-compressed PNG kept the CPU saturated for too long.

Rasta now pays the decoding cost once:

```text
large PNG/JPEG/etc.
    ↓
GDAL sequential decode
    ↓
temporary 512 × 512 tiled BigTIFF working raster
    ↓
power-of-two internal overviews
    ↓
QGIS random-access rendering
```

The staging raster is uncompressed for fast random access and deleted after success, failure, or cancellation. The original source remains untouched.

## Overview planning

Power-of-two overviews are built until the longest raster dimension has a compact whole-image overview. For the 29,684 × 7,620 Montreal test, the plan was:

```text
2, 4, 8, 16, 32, 64, 128
```

## Headless QGIS worker

The public Python 3.14.5 process does not attempt to import PyQGIS directly. Rasta launches QGIS's own `python-qgis.bat`, then runs `RPF_QGIS_WORKER.py` inside the tested QGIS environment.

The worker:

1. initializes `QgsApplication` without QGIS Desktop;
2. loads the prepared raster;
3. sets the project CRS to EPSG:3857;
4. transforms real-georaster bounds when required;
5. invokes `native:tilesxyzmbtiles`;
6. emits progress/info records to the controlling GUI;
7. returns the produced MBTiles path.

Frozen rendering recipe:

- QGIS 3.44.9
- raster PNG tiles
- 96 DPI
- antialiasing ON
- metatile 4

## Heartbeat / long-operation visibility

Some QGIS/GDAL stages do not emit trustworthy incremental percentages continuously. Rasta must not invent fake completion percentages.

v0.1.3 therefore adds an independent GUI heartbeat with:

- elapsed wall-clock time;
- current stage name;
- changing activity glyph;
- last meaningful worker message;
- real numeric progress only when the engine provides it.

## MBTiles verification

Before publication, Rasta opens the MBTiles read-only and verifies:

- standard `tiles` columns;
- nonzero tile count;
- min/max zoom;
- raster PNG/JPEG format metadata.

## TPKX converter

`MBTiles_to_TPKX_v0_1_0.py` remains byte-for-byte from the release-accepted Offline GeoStack converter lineage.

SHA-256:

`7e685b396bf2a6a5ca89fdb710b2ae2e25f8e66014e9162408f166b01d78fc97`

The converter writes Esri Compact Cache V2 bundle files and packages them as ZIP64 TPKX. Rasta verifies the TPKX ZIP, required metadata members, Compact Cache V2 storage declaration, and presence of bundle files before publication.

## Cleanup and failure behavior

- single-instance GUI guard;
- QGIS Desktop guard;
- subprocess-tree cancellation;
- temporary work under the system temp directory;
- no overwrite of an existing finished output;
- publish through a partial filename then atomic rename where practical;
- temporary staging removed after success, failure, or cancellation.
