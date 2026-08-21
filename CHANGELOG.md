# Rasta Pyramid Factory Changelog

## 2026-08-20 — TPKX Field Maps compatibility boundary added

A downstream ArcGIS Field Maps control test found a verified compatibility defect in the historical MBTiles -> TPKX converter lineage inherited by Rasta.

- project converter-built TPKX: **Field Maps REJECTED**;
- Esri official `Usa.tpkx`: **Field Maps ACCEPTED** through the same physical-card/Designer workflow.

This does **not** invalidate Rasta v0.1.3's live-proven giant-raster manufacturing or ArcGIS Earth acceptance.

Status correction:

- Rasta v0.1.3 giant-raster core: **LIVE-PROVEN**;
- historical Rasta TPKX -> ArcGIS Earth: **LIVE-PROVEN**;
- historical Rasta TPKX -> Field Maps: **NOT APPROVED / converter repair required**;
- Esri-canonical converter replacement: **upstream BUILT / SELF-TESTED, Field Maps pending**.

The accepted v0.1.3 evidence is preserved unchanged. Once Offline GeoStack's canonical converter passes Field Maps, the corrected TPKX stage will be integrated into a new Rasta test line and regression-tested.

Master engineering record:

https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/TPKX_FIELD_MAPS_CONFORMANCE_2026-08-20.md

---

## 2026-08-18 — deployment separation clarified

- Kept **v0.1.3 TEST** as the current LIVE-PROVEN Rasta baseline.
- Kept **v0.1.4 TEST** as BUILT / SELF-TESTED until real target acceptance.
- Repositioned Map Fountain as LIVE-PROVEN / PARKED from primary personal-phone deployment.
- Recorded the sibling deployment repository: `Android-Field-Maps-and-ArcGIS-Earth-`.
- Clarified that Rasta manufactures pyramids and does not own router/mobile delivery architecture.

## v0.1.4 TEST — 2026-08-17 — BUILT / SELF-TESTED

- Built from the v0.1.3 LIVE-PROVEN baseline.
- Added independent TPKX / MBTiles / REST output selectors.
- QGIS renders MBTiles once; TPKX and REST branch from that verified MBTiles.
- Added Static REST WMTS conversion experiment.
- v0.1.3 remains the live-proven baseline.
- REST is now parked with Map Fountain.

---

## 2026-08-16 — gigapixel / deep-navigation acceptance expansion

### Tower Bridge

- 15,287 x 7,643 JPEG;
- 6,976 tiles;
- Z0-Z18;
- 22 bundles;
- 0:02:18;
- Windows File Explorer TPKX size 294,910 KB;
- ArcGIS Earth PASS.

### Kings Reach Panorama 2

- 63,000 x 18,589 JPEG;
- approximately 1.17 billion source pixels;
- 67,619 tiles;
- Z0-Z18;
- 30 bundles;
- 0:23:07;
- Windows File Explorer TPKX size 1,949,149 KB;
- ArcGIS Earth PASS;
- deep navigation resolved people inside London Eye observation pods.

### Tibidabo / Barcelona

- 62,141 x 14,606 JPEG;
- approximately 908 million source pixels;
- 52,482 tiles;
- Z0-Z18;
- 30 bundles;
- 0:20:40;
- ArcGIS Earth PASS.

### Lessons

- source file megabytes do not predict pyramid size;
- pixel dimensions/total pixels matter more;
- long-stage heartbeat/status behavior is live-proven;
- dense daylight cityscapes are strong demonstrations.

## v0.1.3 TEST — 2026-08-16

- LIVE-PROVEN automatic flat-image path and ArcGIS Earth output.
- Montreal automated run: 29,684 x 7,620, 13,381 tiles, 52 bundles, 0:05:04, ArcGIS Earth PASS.
- Deterministic Atlantic synthetic placement near 30°N / 80°W.
- Independent heartbeat with elapsed time and stage labels.

## v0.1.2 TEST — 2026-08-16

- Added tiled GeoTIFF staging and power-of-two overviews for giant flat images.
- Removed normal GUI manual flat/geo mode selection.

## v0.1.1 TEST — 2026-08-16

- Hardened `gdalinfo -json` parsing against diagnostic/trailing output.

## v0.1.0 TEST — 2026-08-16

- Created Rasta Pyramid Factory.
- Added automatic inspection, synthetic EPSG:3857 placement, headless QGIS MBTiles manufacturing, MBTiles / TPKX / Both outputs, verification, cleanup, and self-test.
- Preserved the historical `MBTiles_to_TPKX_v0_1_0.py` converter lineage then in use.
