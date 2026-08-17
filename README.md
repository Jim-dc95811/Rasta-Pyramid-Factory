# Rasta Pyramid Factory

## Slice. Dice. Present.

**Turn giant raster images into smooth multiscale tile pyramids without manually operating QGIS.**

![ArcGIS Earth Systems — router-only Map Fountain architecture](https://raw.githubusercontent.com/Jim-dc95811/Map-Fountain/main/docs/map_fountain_router_architecture_2026-08-17.svg)

Rasta Pyramid Factory is a Windows-first raster manufacturing tool built around **QGIS 3.44.9 as a headless rendering engine**. Give it a very large flat image or a genuinely georeferenced raster and it manufactures a verified raster pyramid as **MBTiles, TPKX, or both**.

It is not limited to maps. The pixels may represent a city panorama, aerial imagery, a historical scan, drone orthomosaic, scientific raster, artwork, or any other raster QGIS can render.

> **Slice. Dice. Present.**

> **See the whole scene like a hawk. Dive into any detail that catches your eye.**

![Rasta Pyramid Factory v0.1.3 live proof](docs/images/rasta_v0_1_3_live_proof.jpg)

## Status

| Capability | Status |
| --- | --- |
| Manual arbitrary-raster → MBTiles → TPKX architecture | ✅ **LIVE-PROVEN** |
| Automated Rasta v0.1.2 giant PNG → TPKX | ✅ **LIVE-PROVEN** |
| Headless QGIS 3.44.9 tile-pyramid engine | ✅ **LIVE-PROVEN** |
| Frozen MBTiles → Compact Cache V2 / TPKX converter | ✅ **LIVE-PROVEN** |
| Rasta v0.1.3 automatic Atlantic parking + heartbeat | ✅ **LIVE-PROVEN** |
| 63,000 × 18,589 / 1.17-billion-pixel JPEG | ✅ **LIVE-PROVEN** |
| 62,141 × 14,606 Barcelona deep-navigation run | ✅ **LIVE-PROVEN** |
| Long-stage heartbeat during 20+ minute builds | ✅ **LIVE-PROVEN** |

## What the operator does

```text
1. Choose giant raster
2. Choose zoom range
3. Choose MBTiles / TPKX / Both
4. BUILD RASTER PYRAMID
```

Rasta decides automatically whether the source already has real georeferencing. There is no normal-user CRS mode selector and no Georeferencer workflow.

## What Rasta does

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
flat inputs are decoded once into a temporary tiled GeoTIFF
        ↓
working overviews for efficient random access
        ↓
QGIS 3.44.9 headless native:tilesxyzmbtiles
        ↓
verified raster MBTiles pyramid
        ↓
optional frozen Compact Cache V2 converter
        ↓
MBTiles / TPKX / Both
```

The original source raster is not modified.

## Why the pyramid feels different

A few manually chosen image layers can imitate several destination scales, but they do not preserve the journey between those scales.

Rasta manufactures a true multiscale raster pyramid so the viewer can move through neighboring resolution levels continuously. The operator does not choose a detail layer; the viewer requests the appropriate tiles while the operator moves.

That produces the live-observed effect that motivated the project:

```text
whole scene
→ something catches the eye
→ dive toward it
→ more real source detail appears
→ keep moving without losing visual context
```

The pyramid does not invent detail. It makes the detail already present in the source practical to explore.

## Automated live proof — Montreal

On 2026-08-16, Rasta v0.1.2 automatically processed the **29,684 × 7,620** `Montreal_Skyline_from_Mont_Royal_raw.png` source and produced:

- Z0–Z18
- **13,381 raster tiles**
- **52 Compact Cache V2 bundles**
- elapsed: **0:05:04**
- ArcGIS Earth: **PASS**

The overview and deep zoom below are the same manufactured raster pyramid: whole skyline at one scale, then streets, vehicles, roofs, and windows emerging as the viewer moves down the pyramid.

![Montreal overview and deep-zoom live proof](docs/images/montreal_live_proof.jpg)

## Rasta v0.1.3 automated Frankfurt proof

An ordinary **8,003 × 5,622 JPEG** was automatically detected as a flat image, parked at the fixed synthetic Atlantic display anchor near **30°N, 80°W**, manufactured, verified, published, and rendered correctly in ArcGIS Earth.

![Rasta v0.1.3 Frankfurt live proof](docs/images/rasta_v0_1_3_live_proof.jpg)

This moved v0.1.3 itself to **LIVE-PROVEN**.

## Gigapixel-class live proof — London

Rasta v0.1.3 processed `Kings_reach_panorama_2.jpg`:

- **63,000 × 18,589 pixels**
- approximately **1.17 billion source pixels**
- **67,619 final raster tiles**
- Z0–Z18
- **30 bundles**
- elapsed: **0:23:07**
- Windows File Explorer TPKX size: **1,949,149 KB**
- ArcGIS Earth: **PASS**

The overview reads as a normal London panorama. A deep dive toward the London Eye resolves individual people inside the observation pods.

That is the project’s central visual point: **detail that is effectively out of sight at overview scale remains available everywhere the source pixels contain it.**

## Distributed-detail proof — Barcelona

Rasta v0.1.3 processed `Tibidabo.jpg`:

- **62,141 × 14,606 pixels**
- approximately **908 million source pixels**
- **52,482 final tiles**
- Z0–Z18
- **30 bundles**
- elapsed: **0:20:40**
- ArcGIS Earth: **PASS**

Barcelona produced an especially strong “hawk” effect because useful detail is spread across the whole scene. The operator can move from city-wide context into buildings, rooftops, parking lots, cars, construction equipment, balconies, trees, and road geometry in many different directions.

## Tower Bridge proof

A **15,287 × 7,643 JPEG** produced:

- **6,976 tiles**
- Z0–Z18
- **22 bundles**
- elapsed: **0:02:18**
- Windows File Explorer TPKX size: **294,910 KB**
- ArcGIS Earth: **PASS**

The operator could move from the full bridge scene into small river/shore detail without manually changing image layers.

## Output size: do not use source megabytes as the predictor

A source file’s disk size and its pixel count are different things.

A highly compressed JPEG can contain far more pixels than a much larger TIFF. Rasta output size is driven more strongly by:

1. source pixel dimensions / total pixel count;
2. requested pyramid zoom range;
3. scene complexity and compressibility;
4. tile encoding.

Live example:

- a roughly 100 MB-class London JPEG contained about **1.17 billion pixels** and produced a **1,949,149 KB** TPKX;
- a roughly 288 MB Pittsburgh TIFF inspected at only **8,688 × 5,792 pixels** — about 50 million pixels.

So:

> **Do not judge the source by how many megabytes the file weighs. Judge it by what pixels are actually inside.**

See [Gigapixel proof + output-size guidance](docs/GIGAPIXEL_AND_OUTPUT_SIZE.md).

## Synthetic placement for ordinary photographs

A normal photograph has no honest geographic location. Rasta therefore labels its placement as **synthetic display space**, never as real geography.

The internal rule remains reproducible:

- default scale: **1 source pixel = 1 projected meter**;
- synthetic working CRS: **EPSG:3857**;
- v0.1.3 parks flat images at a fixed synthetic anchor near **30°N, 80°W**, in the Atlantic east of Florida;
- the operator does not choose or edit this placement.

Placement has no effect on the source pixels or pyramid detail. It simply gives GIS tile machinery a deterministic projected rectangle to work with.

## Relationship to ArcGIS Earth / Map Fountain

Rasta itself remains a raster-manufacturing project, not a viewer project.

Its **MBTiles and TPKX outputs are first-class products**. On 2026-08-17, the router-only Map Fountain architecture was live-proven with a native production-scale TPKX on USB SSD attached to a GL.iNet Flint 2. ArcGIS Earth opened that package directly through Samba over Wi-Fi and rendered it successfully.

That downstream proof reinforces the value of manufacturing clean native products: the field router does not need to rerender or understand them.

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
