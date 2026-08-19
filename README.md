# Rasta Pyramid Factory

## Giant raster → smooth multiscale pyramid

**Turn very large flat images and georeferenced rasters into verified MBTiles / TPKX pyramids without manually operating QGIS.**

> **Slice. Dice. Present.**

> **See the whole scene like a hawk. Dive into any detail that catches your eye.**

**Keywords:** raster pyramid, image pyramid, deep zoom, gigapixel, QGIS, MBTiles, TPKX, ArcGIS Earth, georeferenced raster, GeoTIFF, panorama, orthomosaic, aerial imagery, multiscale raster, offline imagery

### Where this fits in the larger journey

Rasta grew from a cross-domain question: **could mature GIS pyramid machinery be used for giant ordinary images without pretending those images were real geography?** The answer became deterministic synthetic display space for flat images, preserved real georeferencing for true georasters, and one headless QGIS manufacturing path for both.

That bridge is documented in **[The Bridges We Had to Build](https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/THE_BRIDGES_WE_HAD_TO_BUILD.md)**. The wider firefighter/dispatch/human-AI project story is in **[The Journey of Ideas](https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/JOURNEY_OF_IDEAS.md)**.

![Rasta Pyramid Factory v0.1.3 live proof](docs/images/rasta_v0_1_3_live_proof.jpg)

---

## Current version truth

### v0.1.3 TEST — LIVE-PROVEN core

The current live-proven Rasta baseline remains **v0.1.3**:

- automatic flat-image / georaster inspection;
- tiled staging + overviews for giant flat images;
- headless QGIS 3.44.9 raster-pyramid manufacturing;
- verified raster MBTiles;
- frozen MBTiles → Compact Cache V2 / TPKX converter;
- deterministic synthetic placement for ordinary flat images;
- long-stage heartbeat / elapsed-time behavior;
- live ArcGIS Earth acceptance across multiple large city images.

### v0.1.4 TEST — historical output-selection experiment

A later `Rasta_Pyramid_Factory_v0_1_4_TEST` branch added independent output choices for:

```text
TPKX
MBTiles
REST
```

Its selector/converter logic is **BUILT / SELF-TESTED**, but the REST branch came from the now-parked Map Fountain experiment and is **not the current Rasta direction**.

Do not describe v0.1.4 REST output as LIVE-PROVEN.

---

## Status

| Capability | Status |
| --- | --- |
| Arbitrary raster → MBTiles → TPKX architecture | ✅ **LIVE-PROVEN** |
| Automated giant-raster processing | ✅ **LIVE-PROVEN** |
| Headless QGIS 3.44.9 pyramid engine | ✅ **LIVE-PROVEN** |
| MBTiles → Compact Cache V2 / TPKX converter | ✅ **LIVE-PROVEN** |
| Gigapixel-class deep navigation | ✅ **LIVE-PROVEN** |
| v0.1.3 synthetic placement + heartbeat | ✅ **LIVE-PROVEN** |
| v0.1.4 TPKX / MBTiles / REST selector | 🟡 **BUILT / SELF-TESTED HISTORICAL TEST BRANCH** |
| REST output on real mobile target | 🟡 **NOT LIVE-PROVEN / PARKED WITH MAP FOUNTAIN** |

---

## Operator workflow

```text
1. Choose giant raster
2. Choose zoom range
3. Choose finished product(s)
4. BUILD RASTER PYRAMID
```

Rasta distinguishes ordinary flat imagery from genuinely georeferenced raster input automatically. The normal operator does not need a CRS-mode selector or a manual Georeferencer workflow.

The original source raster is not modified.

---

## Manufacturing architecture

```text
giant source raster
→ QGIS/GDAL inspection
→ real georaster? ─ yes → preserve real georeferencing
       │
       no
       ↓
synthetic display placement
→ tiled working GeoTIFF + overviews
→ QGIS 3.44.9 headless pyramid engine
→ verified raster MBTiles
       ├─ preserve MBTiles when selected
       └─ Compact Cache V2 converter → TPKX
```

The old v0.1.4 TEST branch additionally experimented with REST output. That branch is lineage, not the recommended current product story.

---

## Why the pyramid feels different

Rasta manufactures a true multiscale raster pyramid. The viewer moves continuously through neighboring resolution levels instead of manually switching between separate detail layers.

```text
whole scene
→ something catches the eye
→ dive toward it
→ more source detail appears
→ keep moving without losing context
```

The pyramid does **not** invent detail. It makes detail already present in the source practical to explore.

A local pyramid also removes the need to wait on a network request for every new view.

---

## Major live proofs

### Montreal

- 29,684 × 7,620 pixels
- 13,381 raster tiles
- 52 Compact Cache V2 bundles
- Z0–Z18
- 0:05:04 elapsed
- ArcGIS Earth: **PASS**

![Montreal overview and deep-zoom live proof](docs/images/montreal_live_proof.jpg)

### London — gigapixel-class

`Kings_reach_panorama_2.jpg`

- 63,000 × 18,589 pixels
- approximately 1.17 billion source pixels
- 67,619 final raster tiles
- Z0–Z18
- 30 bundles
- 0:23:07 elapsed
- Windows File Explorer TPKX size: **1,949,149 KB**
- ArcGIS Earth: **PASS**

A deep dive toward the London Eye resolved individual people inside the observation pods.

### Barcelona

- 62,141 × 14,606 pixels
- approximately 908 million source pixels
- 52,482 final tiles
- Z0–Z18
- 30 bundles
- 0:20:40 elapsed
- ArcGIS Earth: **PASS**

### Tower Bridge

- 15,287 × 7,643 pixels
- 6,976 tiles
- Z0–Z18
- 22 bundles
- 0:02:18 elapsed
- Windows File Explorer TPKX size: **294,910 KB**
- ArcGIS Earth: **PASS**

---

## Source-size lesson

A source file’s compressed disk size is a poor predictor of pyramid size. Pixel dimensions, total pixel count, requested zoom range, scene complexity, and tile encoding matter much more.

> **Do not judge the source by how many megabytes the file weighs. Judge it by what pixels are actually inside.**

See [Gigapixel proof + output-size guidance](docs/GIGAPIXEL_AND_OUTPUT_SIZE.md).

---

## Synthetic placement for ordinary images

A normal photograph has no honest geographic location. Rasta therefore labels its placement as **synthetic display space**, never as real geography.

Current reproducible rule:

```text
1 source pixel = 1 projected meter
working CRS = EPSG:3857
fixed synthetic Atlantic anchor near 30°N, 80°W
```

Placement changes no source pixels. It simply gives GIS tile machinery a deterministic projected rectangle.

---

## Requirements

- Windows 10/11 64-bit
- Python 3.14.5 64-bit
- QGIS 3.44.9

The normal GUI does not require the operator to open QGIS Desktop. Rasta launches the QGIS environment invisibly for rendering.

---

## Deployment boundary

Rasta manufactures raster pyramids. It does **not** own field-delivery hardware or the normal user-deployment workflow.

Finished Rasta products may ride on local storage when useful—for example cityscapes, historical scans, specialty imagery, drone orthomosaics, or other large visual references—but deployment belongs downstream.

One downstream use is training: deep, smooth access to large imagery can support the project's **Wildland Imagery University** concept when the source material is appropriate. The training branch lives in the deployment repository rather than inside Rasta itself.

---

## Four-project family

1. **[Offline GeoStack](https://github.com/Jim-dc95811/Offline-GeoStack)** — master map manufacturing + field-system integration.
2. **Rasta Pyramid Factory** — giant-raster / deep-zoom pyramid manufacturing.
3. **[Map Fountain](https://github.com/Jim-dc95811/Map-Fountain)** — LIVE-PROVEN shared-storage/network delivery evidence; currently parked from the normal personal-phone path.
4. **[Android Field Maps + ArcGIS Earth](https://github.com/Jim-dc95811/Android-Field-Maps-and-ArcGIS-Earth-)** — deployment to the user: Android offline maps + Windows ArcGIS Earth field features + imagery training.

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
- [The Journey of Ideas](https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/JOURNEY_OF_IDEAS.md)
- [The Bridges We Had to Build](https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/THE_BRIDGES_WE_HAD_TO_BUILD.md)

---

## Licensing boundary

Original Rasta software and documentation are provided under the MIT License unless a file states otherwise. That license does not grant rights to third-party source imagery or viewer software. Users remain responsible for the rights and terms governing whatever raster they feed into the Factory.

---

# Rasta Pyramid Factory

> **Take one giant image and give the viewer every useful scale before the user asks for it.**
