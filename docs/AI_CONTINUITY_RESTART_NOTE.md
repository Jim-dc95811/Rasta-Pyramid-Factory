# Rasta Pyramid Factory — AI / Maintainer Restart Note

If coming to this project cold, establish the following before changing code.

## Current truth

Rasta is an independent **general raster-pyramid manufacturing** project.

Its core job remains converting large flat images and real georasters into verified multiscale MBTiles and, when selected, TPKX products.

### v0.1.3 TEST

Still **LIVE-PROVEN** for:

- giant flat-image automatic path;
- tiled staging and overviews;
- headless QGIS 3.44.9 manufacturing;
- verified MBTiles;
- synthetic Atlantic parking;
- long-stage heartbeat;
- London/Barcelona/Tower Bridge/Montreal workloads;
- TPKX display in ArcGIS Earth.

---

## Critical compatibility update — 2026-08-20

A downstream ArcGIS Field Maps test exposed a verified defect in the historical MBTiles -> TPKX converter lineage used by Rasta v0.1.3.

Control:

```text
project converter TPKX -> Field Maps REJECTED
Esri official Usa.tpkx -> Field Maps ACCEPTED
```

This means:

- do not claim existing Rasta TPKX is Field Maps-conformant;
- do not erase v0.1.3 ArcGIS Earth evidence;
- do not rewrite v0.1.3 in place;
- wait for Offline GeoStack's Esri-canonical converter to pass Field Maps;
- then integrate the accepted converter into a new Rasta test line.

Master record:

https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/TPKX_FIELD_MAPS_CONFORMANCE_2026-08-20.md

---

## Upstream converter repair status

`ESRI_CANONICAL_TPKX_TEST_v0_2_0` is **BUILT / SELF-TESTED — FIELD MAPS PENDING**.

It copies Esri's canonical Web Mercator LOD values and metadata conventions rather than recalculating them.

The next upstream gate is:

```text
small MBTiles
-> canonical v0.2.0 converter
-> small TPKX
-> physical microSD
-> Field Maps PASS
```

Do not adopt the replacement into Rasta before that real target pass.

---

## After upstream PASS

Create a new Rasta test lineage that:

1. replaces only the TPKX packaging stage with the accepted canonical converter;
2. preserves the live-proven raster inspection/staging/QGIS/MBTiles core;
3. runs regression/self-tests;
4. reruns at least one known city specimen;
5. confirms ArcGIS Earth still works;
6. tests Field Maps only if Rasta is going to claim that downstream compatibility.

Do not mutate or relabel the accepted v0.1.3 evidence package.

---

## v0.1.4 TEST

The TPKX / MBTiles / REST selector branch remains BUILT / SELF-TESTED history.

REST is parked with Map Fountain and is not the current priority.

---

## Human-observed Rasta results that remain valid

- London Eye deep zoom resolved individual people inside observation pods.
- Barcelona showed useful detail distributed across the city.
- Smooth pyramid levels support whole-scene -> deep-detail navigation.
- The pyramid exposes source detail; it does not invent detail.

---

## Output-size rule

Do not use source file megabytes as the primary output-size predictor.

Prioritize:

1. width x height;
2. total pixel count;
3. scene complexity;
4. source format/compression;
5. zoom range.

---

## Deployment relationship

Rasta does not own Android deployment.

Current family roles:

- Offline GeoStack — master manufacturing/integration + TPKX conformance repair;
- Rasta — giant-raster pyramid manufacturing;
- Map Fountain — proven router/storage reference, parked;
- Android Field Maps + ArcGIS Earth — real mobile deployment evidence.

---

## Do not regress

- Do not require ordinary users to operate QGIS Desktop.
- Do not random-read giant PNG/JPEG inputs through thousands of QGIS requests; preserve tiled staging + overviews.
- Do not modify source rasters.
- Do not describe synthetic placement as real geography.
- Do not rewrite v0.1.3 history to hide the downstream converter defect.
- Do not claim ArcGIS Earth acceptance proves Field Maps acceptance.
- Do not adopt the new converter before Field Maps proves it.
- Do not fake progress percentages.
- Do not make Rasta dependent on Map Fountain or Field Maps.

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

After the upstream converter gate resolves:

- cancellation during preparation/QGIS rendering;
- MBTiles-only real GUI target;
- TPKX + MBTiles combination target;
- genuine georeferenced raster specimen;
- very large TIFF/BigTIFF specimen;
- disk-space preflight;
- honest source/output size reporting.

---

## Governing principle

> **Rasta manufactures the pyramid. Preserve the proven core, and inherit compatibility claims only after the real target proves them.**
