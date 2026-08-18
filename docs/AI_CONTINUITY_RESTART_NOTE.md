# Rasta Pyramid Factory — AI / Maintainer Restart Note

If coming to this project cold, establish the following before changing code.

## Current truth

Rasta Pyramid Factory is an independent sibling project created from a capability discovered during Offline GeoStack development.

Its job is **general raster-pyramid manufacturing**, not wildfire mapping, GNSS, PRAVE, incident operations, router serving, or Android deployment.

Rasta's practical value is the conversion of a large monolithic raster into a multiscale tile pyramid that a viewer can navigate continuously. The human experience is often described as a **hawk dive**: scan the whole scene, notice something, descend toward it, and let progressively finer real source detail appear without manually changing layers.

---

## Version truth

### v0.1.3 TEST — LIVE-PROVEN baseline

- Manual giant flat raster → QGIS MBTiles → TPKX → ArcGIS Earth: **LIVE-PROVEN**.
- Rasta v0.1.2 automated 29,684 × 7,620 Montreal PNG → 13,381 tiles → 52 bundles → TPKX → ArcGIS Earth: **LIVE-PROVEN**.
- Rasta v0.1.3 automatic flat-image manufacture + Atlantic synthetic parking + verified publication + ArcGIS Earth display: **LIVE-PROVEN**.
- Tower Bridge 15,287 × 7,643 JPEG → 6,976 tiles → ArcGIS Earth: **LIVE-PROVEN**.
- Kings Reach Panorama 2, 63,000 × 18,589 / ~1.17 billion pixels → 67,619 tiles → 30 bundles → 0:23:07 → ArcGIS Earth: **LIVE-PROVEN**.
- Tibidabo / Barcelona, 62,141 × 14,606 / ~908 million pixels → 52,482 tiles → 30 bundles → 0:20:40 → ArcGIS Earth: **LIVE-PROVEN**.
- 20+ minute heartbeat / elapsed-time behavior: **LIVE-PROVEN**.

### v0.1.4 TEST — BUILT / SELF-TESTED

`Rasta_Pyramid_Factory_v0_1_4_TEST` changed finished-product selection to three independent checkboxes:

```text
TPKX
MBTiles
REST
```

Any one, any two, or all three may be selected.

The REST branch converts the verified MBTiles into the Static REST WMTS-compatible directory form explored for Map Fountain.

Status:

- output-selection logic: BUILT / SELF-TESTED;
- REST converter branch: BUILT / SELF-TESTED;
- full real-target v0.1.4 acceptance: NOT YET LIVE-PROVEN;
- REST mobile acceptance from Rasta v0.1.4: NOT YET LIVE-PROVEN.

Do not silently promote v0.1.4 over v0.1.3.

---

## Important human-observed results

- London Eye deep zoom resolved individual people inside observation pods.
- Barcelona demonstrated useful detail distributed across the whole city rather than concentrated on one landmark.
- Smooth neighboring pyramid levels make the viewer feel like movement through one visual space rather than manual layer switching.
- The pyramid does not invent detail; it exposes source detail at useful viewing scales.

---

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

---

## Deployment relationship changed

Map Fountain proved router/storage delivery on both Windows and Android, but is now **PROVEN / PARKED** from the primary personal-phone path.

The current personal-phone deployment work is:

```text
TPKX
→ microSD
→ Android
→ ArcGIS Field Maps / ArcGIS Earth
```

and lives in:

`Jim-dc95811/Android-Field-Maps-and-ArcGIS-Earth-`

Rasta does not own that workflow.

A useful downstream possibility is to fill spare SD-card capacity with Rasta-generated deep-zoom imagery, historical maps, specialty scans, or other large single-raster pyramids. Treat that as optional deployment use, not Rasta core architecture.

---

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
- Do not make Rasta dependent on Map Fountain or the Android deployment architecture.
- Do not label v0.1.4 REST work LIVE-PROVEN merely because the converter self-test passes.

---

## Frozen environment

- Windows 10/11 64-bit
- Python 3.14.5
- QGIS 3.44.9
- PNG tile output
- 96 DPI
- antialiasing ON
- metatile 4

---

## Current hardening priorities

Strengthen the general pyramid factory before spending effort on downstream REST experiments:

- cancellation during preparation / QGIS rendering;
- MBTiles-only output on the real GUI target;
- TPKX + MBTiles combination on the real GUI target;
- genuinely georeferenced automatic specimen;
- very large TIFF/BigTIFF automatic specimen;
- conservative disk-space preflight;
- honest source/output size reporting.

---

## Four-project family

1. Offline GeoStack — master field mapping / TPKX manufacturing.
2. Rasta Pyramid Factory — general giant-raster pyramid manufacturing.
3. Map Fountain — proven router/storage experiments; parked reference / possible future Starlink NAS.
4. Android Field Maps + ArcGIS Earth — personal-phone / microSD deployment.

Keep these roles separate.

---

## Cold-start reading order

1. `README.md`
2. this file
3. `docs/ACCEPTANCE_RECORD.md`
4. `docs/GIGAPIXEL_AND_OUTPUT_SIZE.md`
5. `docs/TECHNICAL_ARCHITECTURE.md`
6. `CHANGELOG.md`
7. `ROADMAP.md`
8. newest commits / issues

Report the current status before changing behavior.

---

## Governing principle

> **Rasta manufactures the pyramid. Do not let downstream experiments redefine the factory's core.**
