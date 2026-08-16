# Changelog

## 2026-08-16 — gigapixel / deep-navigation acceptance expansion

Rasta v0.1.3 moved well beyond the initial Frankfurt acceptance and crossed multiple large city-image workloads.

### Tower Bridge

- source: **15,287 × 7,643 JPEG**;
- **6,976 tiles**;
- Z0–Z18;
- **22 bundles**;
- elapsed **0:02:18**;
- Windows File Explorer TPKX size **294,910 KB**;
- ArcGIS Earth **PASS**.

### Kings Reach Panorama 2 — first gigapixel-class run

- source: **63,000 × 18,589 JPEG**;
- approximately **1.17 billion source pixels**;
- **67,619 tiles**;
- Z0–Z18;
- **30 bundles**;
- elapsed **0:23:07**;
- Windows File Explorer TPKX size **1,949,149 KB**;
- ArcGIS Earth **PASS**;
- deep navigation to the London Eye resolved individual people inside observation pods.

### Tibidabo / Barcelona

- source: **62,141 × 14,606 JPEG**;
- approximately **908 million source pixels**;
- **52,482 tiles**;
- Z0–Z18;
- **30 bundles**;
- elapsed **0:20:40**;
- ArcGIS Earth **PASS**;
- distributed detail across the city produced strong whole-city → block/building/vehicle navigation.

### Lessons frozen into documentation

- source file size is not a reliable predictor of Rasta output size;
- pixel dimensions / total pixels are the better first screening metric;
- compressed photographic JPEG can be small on disk while containing enormous image payload;
- the proven PNG pyramid can expand heavily from a highly compressed JPEG source;
- long-stage heartbeat/status behavior is now live-observed on 20+ minute builds;
- dense daylight cityscapes are stronger deep-detail demonstration sources than darkness-heavy scenes.

## v0.1.3 TEST — 2026-08-16

- LIVE-PROVEN on an 8,003 × 5,622 Frankfurt city JPEG: automatic flat-image detection, fixed Atlantic parking near 30°N/80°W, verified TPKX publication, and ArcGIS Earth PASS.
- Records v0.1.2 automated Montreal skyline run as LIVE-PROVEN: 29,684 × 7,620 source, 13,381 Z0–Z18 tiles, 52 bundles, 0:05:04, ArcGIS Earth PASS.
- Moves ordinary flat-image synthetic display parking from longitude/latitude 0,0 to a deterministic Atlantic anchor at **30°N, 80°W**, east of Florida.
- Keeps the 1 source pixel = 1 projected meter default and automatic flat/georaster decision.
- Adds independent GUI heartbeat with continuously updating elapsed time and a changing activity glyph.
- Adds explicit stage labels for raster optimization, working overviews, QGIS pyramid generation, verification, TPKX conversion, packaging, and publication.
- Keeps real QGIS percentages when available but does not invent percentages during opaque long-running stages.
- Adds regression self-test for the Florida synthetic parking center.
- Expands plain-language, technical, acceptance, operator, and AI-continuity documentation.

## v0.1.2 TEST — 2026-08-16

- Fixed giant flat-image performance path discovered during the 29,684 × 7,620 Montreal PNG bench run.
- Flat inputs are decoded once into a temporary 512 × 512 tiled GeoTIFF instead of leaving QGIS to random-read the original PNG/JPEG through a VRT.
- Builds power-of-two internal overview levels before QGIS tile manufacturing.
- Adds cancellable GDAL staging commands and failure diagnostics.
- Removes the normal GUI's AUTO / FLAT / GEO choice block; mode selection is automatic.
- Keeps the original raster untouched and deletes staging data during normal cleanup.
- Adds an overview-plan regression self-test.

## v0.1.1 TEST — 2026-08-16

- Fixed raster inspection failure when GDAL or an image codec emits diagnostic text alongside `gdalinfo -json`.
- Machine-readable GDAL JSON is parsed from stdout separately from stderr diagnostics.
- Added tolerant first-object JSON parsing so harmless trailing output cannot trigger `Extra data`.
- Added regression self-test reproducing the exact trailing-diagnostic failure observed on the 29,684 × 7,620 Montreal skyline PNG.

## v0.1.0 TEST — 2026-08-16

- Created Rasta Pyramid Factory as an independent sibling project.
- Automated the manually proven giant-raster workflow.
- Added QGIS/GDAL raster inspection.
- Added synthetic EPSG:3857 placement for ordinary flat images.
- Added headless QGIS `native:tilesxyzmbtiles` rendering through QGIS's own Python environment.
- Added MBTiles / TPKX / Both output choices.
- Preserved the frozen `MBTiles_to_TPKX_v0_1_0.py` converter byte-for-byte.
- Added verification, partial-output protection, cancellation, temporary-work cleanup, and single-instance GUI protection.
- Added self-test anchored to the 20,634 × 10,317 manual proof: 12,489 tile addresses at Z0–Z18 and recommended max zoom Z18 at 1 m/pixel.
