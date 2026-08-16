# Rasta Pyramid Factory — AI / Maintainer Restart Note

If coming to this project cold, establish the following before changing code.

## Current truth

Rasta Pyramid Factory is an independent sibling project created from a capability discovered during Offline GeoStack development.

Its job is **general raster-pyramid manufacturing**, not wildfire mapping, GNSS, PRAVE, or incident operations.

Rasta’s practical value is the conversion of a large monolithic raster into a multiscale tile pyramid that a viewer can navigate continuously. The human experience is often described as a **hawk dive**: scan the whole scene, notice something, descend toward it, and let progressively finer real source detail appear without manually changing layers.

## Proven baseline

- Manual giant flat raster → QGIS MBTiles → TPKX → ArcGIS Earth: **LIVE-PROVEN**.
- Rasta v0.1.2 automated 29,684 × 7,620 Montreal PNG → 13,381 tiles → 52 bundles → TPKX → ArcGIS Earth: **LIVE-PROVEN**.
- Rasta v0.1.3 automatic flat-image manufacture + Atlantic synthetic parking + verified publication + ArcGIS Earth display: **LIVE-PROVEN**.
- Tower Bridge 15,287 × 7,643 JPEG → 6,976 tiles → ArcGIS Earth: **LIVE-PROVEN**.
- Kings Reach Panorama 2, 63,000 × 18,589 / ~1.17 billion pixels → 67,619 tiles → 30 bundles → 0:23:07 → ArcGIS Earth: **LIVE-PROVEN**.
- Tibidabo / Barcelona, 62,141 × 14,606 / ~908 million pixels → 52,482 tiles → 30 bundles → 0:20:40 → ArcGIS Earth: **LIVE-PROVEN**.
- 20+ minute heartbeat / elapsed-time behavior: **LIVE-PROVEN**.

## Important human-observed results

- London Eye deep zoom resolved individual people inside observation pods.
- Barcelona demonstrated useful detail distributed across the whole city rather than concentrated on one landmark.
- Smooth neighboring pyramid levels make the viewer feel like movement through one visual space rather than manual layer switching.
- The pyramid does not invent detail; it exposes source detail at useful viewing scales.

## Output-size rule

Do **not** use source file megabytes as the primary predictor of Rasta output size.

A highly compressed JPEG can contain far more pixels than a much larger TIFF.

Screen source candidates by:

1. exact width × height;
2. total pixel count;
3. scene complexity / useful detail;
4. source format/compression;
5. requested zoom range.

For public demonstrations, dense daylight cityscapes have been especially effective because recognizable fine detail is spread across the frame.

## Do not regress

- Do not require ordinary users to operate QGIS Desktop.
- Do not restore the removed Auto/Flat/Geo choice block to the normal GUI without a proven need.
- Do not random-read giant PNG/JPEG sources directly through thousands of QGIS tile requests; preserve the tiled staging + overview path.
- Do not modify original source rasters.
- Do not describe synthetic flat-image placement as real geography.
- Do not casually rewrite the frozen MBTiles→TPKX converter.
- Do not fake progress percentages. Use heartbeat/elapsed/stage when progress is unknowable.
- Do not call QGIS metatile/work counts final tile counts.
- Do not make Rasta dependent on ArcGIS Earth; MBTiles is a first-class output.
- Do not recommend a giant demo image without first verifying its actual pixel dimensions.

## Relationship to Map Fountain

Offline GeoStack subsequently proved a local Android deployment path:

```text
MBTiles
→ local HTTPS WMTS
→ Android USB tether
→ ArcGIS Earth Mobile
```

Three substantial MBTiles were displayed, including the large Lago panorama. This is useful downstream validation of MBTiles as a first-class Rasta output, but Map Fountain is not part of Rasta’s core manufacturing responsibility.

## Frozen environment

- Windows 10/11 64-bit
- Python 3.14.5
- QGIS 3.44.9
- PNG tile output
- 96 DPI
- antialiasing ON
- metatile 4

## Remaining v0.1.3 release gates

- cancellation during preparation / QGIS rendering;
- MBTiles-only output through Rasta GUI;
- Both output through Rasta GUI;
- genuinely georeferenced AUTO specimen;
- very large TIFF/BigTIFF automatic specimen;
- conservative disk-space preflight.

## Cold-start reading order

1. `README.md`
2. `docs/ACCEPTANCE_RECORD.md`
3. `docs/GIGAPIXEL_AND_OUTPUT_SIZE.md`
4. `docs/TECHNICAL_ARCHITECTURE.md`
5. `CHANGELOG.md`
6. `ROADMAP.md`
7. newest commits / issues

Report the current status before changing behavior.
