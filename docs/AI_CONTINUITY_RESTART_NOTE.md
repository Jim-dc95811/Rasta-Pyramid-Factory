# Rasta Pyramid Factory — AI / Maintainer Restart Note

If coming to this project cold, establish the following before changing code.

## Current truth

Rasta Pyramid Factory is an independent sibling project created from a capability discovered during Offline GeoStack development.

Its job is **general raster-pyramid manufacturing**, not wildfire mapping, GNSS, PRAVE, or incident operations.

## Proven baseline

- Manual giant flat raster → QGIS MBTiles → TPKX → ArcGIS Earth: **LIVE-PROVEN**.
- Rasta v0.1.2 automated 29,684 × 7,620 Montreal PNG → 13,381 tiles → 52 bundles → TPKX → ArcGIS Earth: **LIVE-PROVEN**.
- Rasta v0.1.3 automatic flat-image manufacture + Atlantic synthetic parking + verified TPKX publication + ArcGIS Earth display: **LIVE-PROVEN**.

## Do not regress

- Do not require ordinary users to operate QGIS Desktop.
- Do not restore the removed Auto/Flat/Geo choice block to the normal GUI without a proven need.
- Do not random-read giant PNG/JPEG sources directly through thousands of QGIS tile requests; preserve the tiled staging + overview path.
- Do not modify original source rasters.
- Do not describe synthetic flat-image placement as real geography.
- Do not casually rewrite the frozen MBTiles→TPKX converter.
- Do not fake progress percentages. Use heartbeat/elapsed/stage when progress is unknowable.
- Do not make Rasta dependent on ArcGIS Earth; MBTiles is a first-class output for other viewers.

## Frozen environment

- Windows 10/11 64-bit
- Python 3.14.5
- QGIS 3.44.9
- PNG tile output
- 96 DPI
- antialiasing ON
- metatile 4

## Cold-start reading order

1. `README.md`
2. `docs/ACCEPTANCE_RECORD.md`
3. `docs/TECHNICAL_ARCHITECTURE.md`
4. `CHANGELOG.md`
5. `ROADMAP.md`
6. newest commits / issues once the GitHub repository exists

Report the current status before changing behavior.
