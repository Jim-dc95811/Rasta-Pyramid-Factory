# Rasta Pyramid Factory

## Giant raster -> smooth multiscale pyramid

**Turn very large flat images and georeferenced rasters into verified MBTiles / TPKX pyramids without manually operating QGIS.**

> **Slice. Dice. Present.**

> **See the whole scene like a hawk. Dive into any detail that catches your eye.**

---

## Current version truth

### v0.1.3 TEST — LIVE-PROVEN core

Rasta v0.1.3 remains **LIVE-PROVEN** for:

- automatic flat-image / georaster inspection;
- tiled staging + overviews for giant flat images;
- headless QGIS 3.44.9 pyramid manufacturing;
- verified raster MBTiles;
- deterministic synthetic placement for ordinary flat images;
- long-build heartbeat;
- large/gigapixel workloads;
- TPKX output rendered successfully in **ArcGIS Earth**.

### Important TPKX compatibility boundary — 2026-08-20

A downstream ArcGIS Field Maps control test found a verified defect in the historical MBTiles -> TPKX converter lineage that Rasta v0.1.3 inherited.

Using the same physical-card/Designer workflow, Field Maps:

- rejected a project converter-built TPKX;
- accepted Esri's official `Usa.tpkx`.

Therefore Rasta's existing TPKX output remains **ArcGIS Earth-proven**, but **Field Maps compatibility is not approved** until the Esri-canonical converter repair is proven and integrated.

Rasta's MBTiles manufacturing and giant-raster core are not invalidated by this finding.

See the master engineering record:

- [Offline GeoStack — TPKX / Field Maps Conformance](https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/TPKX_FIELD_MAPS_CONFORMANCE_2026-08-20.md)

---

## Current status

| Capability | Status |
| --- | --- |
| Automated giant-raster processing | ✅ **LIVE-PROVEN** |
| Headless QGIS 3.44.9 pyramid engine | ✅ **LIVE-PROVEN** |
| Raster -> verified MBTiles | ✅ **LIVE-PROVEN** |
| Historical MBTiles -> TPKX -> ArcGIS Earth | ✅ **LIVE-PROVEN** |
| Historical Rasta TPKX -> Field Maps | ❌ **NOT APPROVED — converter lineage failed Field Maps** |
| Esri-canonical replacement converter | 🟡 **BUILT / SELF-TESTED IN OFFLINE GEOSTACK; FIELD MAPS PENDING** |
| Gigapixel-class deep navigation | ✅ **LIVE-PROVEN** |
| v0.1.3 synthetic placement + heartbeat | ✅ **LIVE-PROVEN** |
| v0.1.4 TPKX / MBTiles / REST selector | 🟡 **BUILT / SELF-TESTED HISTORICAL TEST BRANCH** |
| REST output | ⏸️ **PARKED WITH MAP FOUNTAIN** |

---

## Operator workflow

```text
1. Choose giant raster
2. Choose zoom range
3. Choose finished product(s)
4. BUILD RASTER PYRAMID
```

Rasta distinguishes ordinary flat imagery from genuinely georeferenced raster input automatically. The normal operator does not need a CRS-mode selector or manual Georeferencer workflow.

The original source raster is not modified.

---

## Manufacturing architecture

```text
giant source raster
-> QGIS/GDAL inspection
-> real georaster? -> preserve real georeferencing
       |
       no
       v
synthetic display placement
-> tiled working GeoTIFF + overviews
-> QGIS 3.44.9 headless pyramid engine
-> verified raster MBTiles
       |-- preserve MBTiles when selected
       `-- TPKX converter -> TPKX
```

### Current converter rule

For ArcGIS Earth, the v0.1.3 historical TPKX output remains proven evidence.

For future production and any Field Maps claim, Rasta must adopt the replacement converter only after the Esri-canonical small specimen passes Field Maps.

Do not rewrite the accepted v0.1.3 evidence package and pretend it was always the new converter.

---

## Major live proofs

### Montreal

- 29,684 x 7,620 pixels
- 13,381 raster tiles
- 52 bundles
- Z0-Z18
- 0:05:04
- ArcGIS Earth: PASS

### London — gigapixel-class

`Kings_reach_panorama_2.jpg`

- 63,000 x 18,589 pixels
- approximately 1.17 billion source pixels
- 67,619 final raster tiles
- Z0-Z18
- 30 bundles
- 0:23:07
- Windows File Explorer TPKX size: 1,949,149 KB
- ArcGIS Earth: PASS

Deep navigation resolved individual people inside London Eye observation pods.

### Barcelona

- 62,141 x 14,606 pixels
- approximately 908 million source pixels
- 52,482 final tiles
- Z0-Z18
- 30 bundles
- 0:20:40
- ArcGIS Earth: PASS

### Tower Bridge

- 15,287 x 7,643 pixels
- 6,976 tiles
- Z0-Z18
- 22 bundles
- 0:02:18
- Windows File Explorer TPKX size: 294,910 KB
- ArcGIS Earth: PASS

---

## Source-size lesson

A source file's compressed disk size is a poor predictor of pyramid size. Pixel dimensions, total pixel count, scene complexity, zoom range, and encoding matter more.

---

## Synthetic placement for ordinary images

A normal photograph has no honest geographic location. Rasta labels its placement as **synthetic display space**.

Current reproducible rule:

```text
1 source pixel = 1 projected meter
working CRS = EPSG:3857
fixed synthetic Atlantic anchor near 30°N, 80°W
```

---

## Requirements

- Windows 10/11 64-bit
- Python 3.14.5 64-bit
- QGIS 3.44.9

---

## Deployment boundary

Rasta manufactures raster pyramids. It does not own field-delivery hardware or Field Maps compatibility policy.

Deployment belongs downstream in the Android Field Maps + ArcGIS Earth repository.

The current converter repair belongs in Offline GeoStack, then propagates into Rasta after real-target proof.

---

## Four-project family

1. [Offline GeoStack](https://github.com/Jim-dc95811/Offline-GeoStack) — master manufacturing/integration + current TPKX conformance repair.
2. **Rasta Pyramid Factory** — giant-raster/deep-zoom manufacturing.
3. [Map Fountain](https://github.com/Jim-dc95811/Map-Fountain) — LIVE-PROVEN shared-storage/network reference; parked.
4. [Android Field Maps + ArcGIS Earth](https://github.com/Jim-dc95811/Android-Field-Maps-and-ArcGIS-Earth-) — deployment and real Field Maps acceptance evidence.

---

## Documentation

- [Plain-language overview](docs/PLAIN_LANGUAGE_OVERVIEW.md)
- [Operator workflow](docs/OPERATOR_WORKFLOW.md)
- [Technical architecture](docs/TECHNICAL_ARCHITECTURE.md)
- [Live acceptance record](docs/ACCEPTANCE_RECORD.md)
- [Gigapixel + output-size guidance](docs/GIGAPIXEL_AND_OUTPUT_SIZE.md)
- [AI / maintainer restart note](docs/AI_CONTINUITY_RESTART_NOTE.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

---

## Governing rule

> **Rasta manufactures the pyramid. The real target decides compatibility. Do not let downstream deployment claims outrun evidence.**
