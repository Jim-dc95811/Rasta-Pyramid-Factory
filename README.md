# Rasta Pyramid Factory

## Slice. Dice. Present.

**Turn giant raster images into smooth multiscale tile pyramids without manually operating QGIS.**

![Canonical ArcGIS Earth Systems router flowchart](https://raw.githubusercontent.com/Jim-dc95811/Map-Fountain/main/docs/arcgis_system_router_flowchart_2026-08-17.svg)

Rasta Pyramid Factory is a Windows-first raster manufacturing tool built around **QGIS 3.44.9 as a headless rendering engine**. Give it a very large flat image or a genuinely georeferenced raster and it manufactures a verified raster pyramid as **MBTiles, TPKX, or both**.

It is not limited to maps. The pixels may represent a city panorama, aerial imagery, a historical scan, drone orthomosaic, scientific raster, artwork, or any other raster QGIS can render.

> **Slice. Dice. Present.**

> **See the whole scene like a hawk. Dive into any detail that catches your eye.**

![Rasta Pyramid Factory v0.1.3 live proof](docs/images/rasta_v0_1_3_live_proof.jpg)

## Status

| Capability | Status |
| --- | --- |
| Manual arbitrary-raster → MBTiles → TPKX architecture | ✅ **LIVE-PROVEN** |
| Automated giant-raster processing | ✅ **LIVE-PROVEN** |
| Headless QGIS 3.44.9 tile-pyramid engine | ✅ **LIVE-PROVEN** |
| Frozen MBTiles → Compact Cache V2 / TPKX converter | ✅ **LIVE-PROVEN** |
| Gigapixel-class deep-navigation output | ✅ **LIVE-PROVEN** |
| MBTiles / TPKX / Both finished-product choices | ✅ **LIVE-PROVEN architecture** |

## Operator workflow

```text
1. Choose giant raster
2. Choose zoom range
3. Choose MBTiles / TPKX / Both
4. BUILD RASTER PYRAMID
```

Rasta automatically distinguishes ordinary flat imagery from genuinely georeferenced raster input. The normal operator does not need a CRS-mode selector or a manual Georeferencer workflow.

## Manufacturing architecture

```text
giant source raster
        ↓
QGIS/GDAL inspection
        ↓
real georaster? ── yes ── preserve real georeferencing
        │
        no
        ↓
synthetic display placement
        ↓
flat input staged into tiled working GeoTIFF
        ↓
working overviews
        ↓
QGIS 3.44.9 headless tile-pyramid engine
        ↓
verified raster MBTiles
        ↓
optional frozen Compact Cache V2 converter
        ↓
MBTiles / TPKX / Both
```

The original source raster is not modified.

## Why the pyramid feels different

Rasta manufactures a true multiscale raster pyramid. The operator moves continuously through neighboring resolution levels instead of manually selecting separate detail layers.

```text
whole scene
→ something catches the eye
→ dive toward it
→ more real source detail appears
→ keep moving without losing context
```

The pyramid does not invent detail. It makes the detail already present in the source practical to explore.

## Major live proofs

### Montreal

- **29,684 × 7,620** pixels
- **13,381 raster tiles**
- **52 Compact Cache V2 bundles**
- Z0–Z18
- elapsed **0:05:04**
- ArcGIS Earth: **PASS**

![Montreal overview and deep-zoom live proof](docs/images/montreal_live_proof.jpg)

### London — gigapixel-class

`Kings_reach_panorama_2.jpg`

- **63,000 × 18,589 pixels**
- approximately **1.17 billion source pixels**
- **67,619 final raster tiles**
- Z0–Z18
- **30 bundles**
- elapsed **0:23:07**
- Windows File Explorer TPKX size **1,949,149 KB**
- ArcGIS Earth: **PASS**

A deep dive toward the London Eye resolved individual people inside the observation pods.

### Barcelona

- **62,141 × 14,606 pixels**
- approximately **908 million source pixels**
- **52,482 final tiles**
- Z0–Z18
- **30 bundles**
- elapsed **0:20:40**
- ArcGIS Earth: **PASS**

### Tower Bridge

- **15,287 × 7,643** pixels
- **6,976 tiles**
- Z0–Z18
- **22 bundles**
- elapsed **0:02:18**
- Windows File Explorer TPKX size **294,910 KB**
- ArcGIS Earth: **PASS**

## Source-size lesson

A source file's disk size is a poor predictor of pyramid size. Pixel dimensions, total pixel count, requested zoom range, scene complexity, and tile encoding matter much more.

> **Do not judge the source by how many megabytes the file weighs. Judge it by what pixels are actually inside.**

See [Gigapixel proof + output-size guidance](docs/GIGAPIXEL_AND_OUTPUT_SIZE.md).

## Synthetic placement for ordinary photographs

A normal photograph has no honest geographic location. Rasta therefore labels its placement as **synthetic display space**, never as real geography.

Current reproducible rule:

- default scale: **1 source pixel = 1 projected meter**;
- synthetic working CRS: **EPSG:3857**;
- flat images are parked at a fixed synthetic Atlantic anchor near **30°N, 80°W**;
- the operator does not choose or edit this placement.

Placement changes no source pixels. It simply gives GIS tile machinery a deterministic projected rectangle.

## Relationship to Map Fountain

Rasta manufactures finished native products. **Map Fountain carries them. ArcGIS Earth consumes them.**

On 2026-08-17 the router-only Map Fountain architecture was LIVE-PROVEN with a production-scale native TPKX stored on a USB SSD attached to a GL.iNet Flint 2. ArcGIS Earth opened that package directly through Samba over Wi-Fi and rendered it successfully.

That is the architectural payoff: the field router does not need to understand, unpack, or rerender Rasta products.

The router-only Android path is the next Map Fountain acceptance gate; Rasta itself remains a manufacturing project and does not own that client-compatibility problem.

## Requirements

- Windows 10/11 64-bit
- Python 3.14.5 64-bit
- QGIS 3.44.9

The normal GUI does not require the operator to open QGIS Desktop. Rasta launches QGIS's own Python environment invisibly for rendering.

## Documentation

- [Plain-language overview](docs/PLAIN_LANGUAGE_OVERVIEW.md)
- [Operator workflow](docs/OPERATOR_WORKFLOW.md)
- [Technical architecture](docs/TECHNICAL_ARCHITECTURE.md)
- [Live acceptance record](docs/ACCEPTANCE_RECORD.md)
- [Gigapixel + output-size guidance](docs/GIGAPIXEL_AND_OUTPUT_SIZE.md)
- [AI / maintainer restart note](docs/AI_CONTINUITY_RESTART_NOTE.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

## Project relationship

Rasta Pyramid Factory was discovered while developing **Offline GeoStack**, but it stands on its own. Offline GeoStack needed an offline map-manufacturing chain; Rasta generalizes the raster-pyramid part into a viewer-independent manufacturing tool.

## License and source imagery

Original Rasta software and documentation are provided under the MIT License unless a file states otherwise. That license does not grant rights to third-party source imagery or viewer software. Users remain responsible for the rights and terms governing whatever raster they feed into the Factory.
