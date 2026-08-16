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

This moved **v0.1.3 TEST** from BUILT/SELF-TESTED to **LIVE-PROVEN** for automatic synthetic placement, manufacture, verification, publication, and ArcGIS Earth display.

## Tower Bridge automated proof — 2026-08-16

**Status: LIVE-PROVEN**

Source:
- `Tower_Bridge_from_Shad_Thames.jpg`
- **15,287 × 7,643 pixels**
- ordinary JPEG

Observed result:
- **6,976 tiles**
- **Z0–Z18**
- **22 bundles**
- elapsed: **0:02:18**
- Windows File Explorer TPKX size: **294,910 KB**
- ArcGIS Earth full-scene display: **PASS**
- ArcGIS Earth deep river/shore detail: **PASS**

The viewer preserved continuous navigation from the whole bridge scene into small details without manual resolution-layer switching.

## First gigapixel-class automated proof — Kings Reach Panorama 2 — 2026-08-16

**Status: LIVE-PROVEN**

Source:
- `Kings_reach_panorama_2.jpg`
- **63,000 × 18,589 pixels**
- approximately **1.17 billion source pixels**
- ordinary JPEG

Observed result:
- **67,619 tiles**
- **Z0–Z18**
- **30 bundles**
- elapsed: **0:23:07**
- Windows File Explorer TPKX size: **1,949,149 KB**
- ArcGIS Earth overview: **PASS**
- ArcGIS Earth deep navigation: **PASS**

Human-observed detail result:
- the London Eye is a small feature in the overview;
- after diving through the pyramid, individual people were visible inside observation pods.

This is the first automated **gigapixel-class** Rasta acceptance specimen.

## Barcelona / Tibidabo distributed-detail proof — 2026-08-16

**Status: LIVE-PROVEN**

Source:
- `Tibidabo.jpg`
- **62,141 × 14,606 pixels**
- approximately **908 million source pixels**
- ordinary JPEG

Observed result:
- **52,482 tiles**
- **Z0–Z18**
- **30 bundles**
- elapsed: **0:20:40**
- ArcGIS Earth overview: **PASS**
- ArcGIS Earth deep navigation: **PASS**

Human-observed detail result:
- detail remained useful across many different directions in the frame;
- buildings, roofs, cars, parking areas, construction equipment, balconies, trees, and road geometry emerged during deliberate navigation.

This specimen is especially valuable because the deep-detail effect is not dependent on one famous landmark; useful source detail is distributed across the city.

## Long-stage heartbeat acceptance

**Status: LIVE-PROVEN**

The 20+ minute Kings Reach / Barcelona manufacturing runs confirmed that the v0.1.3 GUI heartbeat and elapsed-time reporting remain visibly active during long QGIS work. The operator can distinguish an active long build from a frozen application.

QGIS may report internal work/metatile counts that are not the final raster-tile count. Future UI wording should continue to distinguish QGIS work units from final tile counts rather than presenting them as the same metric.

## Output-size lesson from live specimens

**Status: LIVE-OBSERVED / DOCUMENTED**

Source file size is not a reliable predictor of finished pyramid size.

- A roughly 100 MB-class Kings Reach JPEG contained about 1.17 billion pixels and produced a **1,949,149 KB** TPKX.
- A roughly 288 MB Pittsburgh TIFF inspected at only **8,688 × 5,792 pixels** — about 50 million pixels.

For source screening and rough planning, use pixel dimensions / total pixel count before source-file megabytes.

## Remaining release-hardening work

The following remain separate from the live acceptance results above:

- cancellation testing;
- Rasta GUI MBTiles-only output testing;
- Rasta GUI Both-output testing;
- genuinely georeferenced AUTO-mode specimen;
- very large TIFF/BigTIFF automatic specimen;
- conservative disk-space preflight.
