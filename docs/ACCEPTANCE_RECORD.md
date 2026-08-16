# Rasta Pyramid Factory — Acceptance Record

## Evidence labels

**LIVE-PROVEN** — observed on the real Windows/QGIS target and accepted by the intended viewer/workflow.

**BUILT / SELF-TESTED** — code exists and passes internal/static tests but has not yet crossed the live target gate.

## Manual arbitrary-raster architecture proof — 2026-08-16

**Status: LIVE-PROVEN**

Source:
- 20,634 × 10,317 HDR panorama
- approximately 3.2 GB source file
- ordinary non-geographic image

Manual preparation:
- synthetic EPSG:3857 display space
- 1 source pixel = 1 projected meter
- initial proof centered at 0,0

QGIS recipe:
- QGIS 3.44.9
- Generate XYZ tiles (MBTiles)
- Z0–Z18
- PNG
- 96 DPI
- antialiasing ON
- metatile 4

Observed finished TPKX:
- **12,489 tiles**
- **52 Compact Cache V2 bundles**
- Windows File Explorer size: **556,781 KB**
- converter elapsed: **0:00:18**
- ArcGIS Earth: **PASS**

This proved the general architecture: a giant ordinary flat raster can be assigned deterministic synthetic display coordinates, manufactured into a true multiscale raster pyramid, converted to TPKX, and rendered by ArcGIS Earth.

## Rasta v0.1.2 automated Montreal proof — 2026-08-16

**Status: LIVE-PROVEN**

Source:
- `Montreal_Skyline_from_Mont_Royal_raw.png`
- **29,684 × 7,620 pixels**
- ordinary non-geographic PNG

Rasta automation:
- source automatically detected as flat image;
- synthetic projected display space generated automatically;
- source decoded once into optimized tiled working GeoTIFF;
- working overviews generated;
- QGIS 3.44.9 launched headlessly;
- Z0–Z18 raster MBTiles manufactured;
- MBTiles verified;
- frozen converter produced TPKX;
- TPKX verified and published.

Observed result:
- **13,381 tiles**
- **52 Compact Cache V2 bundles**
- elapsed: **0:05:04**
- ArcGIS Earth overview: **PASS**
- ArcGIS Earth deep zoom to streets/windows/vehicles: **PASS**

Evidence image:
- `docs/images/montreal_live_proof.jpg`

This moved the automated Rasta pipeline from BUILT/SELF-TESTED to **LIVE-PROVEN**.

## Rasta v0.1.3 automated Frankfurt proof — 2026-08-16

**Status: LIVE-PROVEN**

Source:
- `Skyline_Frankfurt_am_Main_2015.jpg`
- **8,003 × 5,622 pixels**
- ordinary non-geographic JPEG

Observed v0.1.3 behavior:
- source automatically detected as a flat image;
- synthetic display parking moved automatically to the fixed **30°N, 80°W** Atlantic anchor east of Florida;
- normal GUI exposed no flat/georaster/CRS placement choice;
- raster pyramid manufacture completed and the product was verified and published;
- ArcGIS Earth rendered the finished product correctly;
- ArcGIS Earth status bar showed the synthetic product near **30°N, 80°W**, confirming the live parking-anchor change.

Evidence image:
- `docs/images/rasta_v0_1_3_live_proof.jpg`

This moves **v0.1.3 TEST** from BUILT/SELF-TESTED to **LIVE-PROVEN** for automatic synthetic placement, manufacture, verification, publication, and ArcGIS Earth display.

The remaining release-hardening work is separate from this acceptance result: cancellation testing, MBTiles-only/Both output testing, disk-space preflight, and broader source-format coverage.
