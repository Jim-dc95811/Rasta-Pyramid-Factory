# Rasta Pyramid Factory

## Slice. Dice. Present.

**Turn giant raster images into smooth multiscale tile pyramids without manually operating QGIS.**

Rasta Pyramid Factory is a Windows-first raster manufacturing tool built around **QGIS 3.44.9 as a headless rendering engine**. Give it a very large flat image or a genuinely georeferenced raster and it manufactures a verified raster pyramid as **MBTiles, TPKX, or both**.

It is not limited to maps. The pixels may represent a city panorama, aerial imagery, a historical scan, drone orthomosaic, scientific raster, artwork, or any other raster QGIS can render.

> **Slice. Dice. Present.**

![Rasta v0.1.2 automated completion](docs/images/rasta_v0_1_2_complete.png)

## Status

| Capability | Status |
| --- | --- |
| Manual arbitrary-raster → MBTiles → TPKX architecture | ✅ **LIVE-PROVEN** |
| Automated Rasta v0.1.2 giant PNG → TPKX | ✅ **LIVE-PROVEN** |
| Headless QGIS 3.44.9 tile-pyramid engine | ✅ **LIVE-PROVEN** |
| Frozen MBTiles → Compact Cache V2 / TPKX converter | ✅ **LIVE-PROVEN** |
| Rasta v0.1.3 Florida synthetic parking + heartbeat | ✅ **LIVE-PROVEN** |

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

## First automated live proof — Montreal

On 2026-08-16, Rasta v0.1.2 automatically processed the **29,684 × 7,620** `Montreal_Skyline_from_Mont_Royal_raw.png` source and produced:

- Z0–Z18
- **13,381 raster tiles**
- **52 Compact Cache V2 bundles**
- elapsed: **0:05:04**
- ArcGIS Earth: **PASS**

The overview image and deep zoom below are the same manufactured raster pyramid.

![Montreal panorama overview in ArcGIS Earth](docs/images/montreal_arcgis_earth_overview.png)

![Montreal deep zoom in ArcGIS Earth](docs/images/montreal_arcgis_earth_deep_zoom.png)

That is the point of a raster pyramid: a viewer does not need to treat the source as one monolithic image. It requests only the resolution level and tile region needed for the current view.

## Second automated live proof — Frankfurt

On 2026-08-16, **Rasta v0.1.3 TEST** processed an ordinary **8,003 × 5,622 JPEG** city image with no manual georeferencing controls exposed to the operator. Rasta automatically placed the synthetic display space at its fixed Atlantic parking anchor east of Florida, manufactured and verified the raster pyramid, published the TPKX, and ArcGIS Earth rendered the result correctly.

The ArcGIS Earth status bar shows the synthetic placement near **30°N, 80°W**, confirming that the v0.1.3 parking-anchor change is working on the live target.

![Rasta v0.1.3 Frankfurt completion](docs/images/rasta_v0_1_3_frankfurt_complete.png)

![Frankfurt raster pyramid in ArcGIS Earth](docs/images/frankfurt_arcgis_earth.png)

This confirms that v0.1.3 is **LIVE-PROVEN** for automatic flat-image placement, manufacture, verification, publication, and ArcGIS Earth display.

## Synthetic placement for ordinary photographs

A normal photograph has no honest geographic location. Rasta therefore labels its placement as **synthetic display space**, never as real geography.

The internal rule remains reproducible:

- default scale: **1 source pixel = 1 projected meter**;
- CRS used for the synthetic working raster: **EPSG:3857**;
- v0.1.3 parks flat images at a fixed synthetic anchor near **30°N, 80°W**, in the Atlantic east of Florida, instead of lon/lat 0,0 off Africa;
- the operator does not choose or edit this placement.

Placement has no effect on the source pixels or pyramid detail. It simply gives GIS tile machinery a deterministic projected rectangle to work with.

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
- [AI / maintainer restart note](docs/AI_CONTINUITY_RESTART_NOTE.md)
- [Roadmap](ROADMAP.md)
- [Changelog](CHANGELOG.md)

## Project relationship

Rasta Pyramid Factory was discovered while developing **Offline GeoStack**, but it stands on its own. Offline GeoStack needed an offline map-manufacturing chain; Rasta generalizes the raster-pyramid part into a viewer-independent manufacturing tool.

## License and source imagery

Original Rasta software and documentation are provided under the MIT License unless a file states otherwise. That license does not grant rights to third-party source imagery or viewer software. Users remain responsible for the rights and terms governing whatever raster they feed into the Factory.
