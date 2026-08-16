# Rasta Pyramid Factory — Plain-Language Overview

## The problem

A giant image can contain far more detail than one screen can show at once. Conventional image viewers often treat that source as one enormous picture and repeatedly scale or decode it as the user zooms and pans. With very large images, that can become slow, memory-heavy, or impractical.

A **raster pyramid** approaches the problem differently.

The source is manufactured into many small image tiles at multiple resolution levels. When the viewer is zoomed far out, it uses a small overview. When the viewer zooms in, it replaces that overview with progressively more detailed tiles. At the deepest useful level, the tiles approach the detail of the original source.

```text
one enormous source image
        ↓
small whole-image overview
        ↓
medium-resolution tiles
        ↓
higher-resolution tiles
        ↓
source-detail tiles
```

The viewer therefore does not need the whole original image decoded at full resolution merely to show one small part of it.

## What Rasta changes

Rasta turns the manufacturing process into an appliance:

```text
choose image → BUILD → open finished tiled product
```

The operator does not need to:

- calculate artificial extents;
- create world files;
- use QGIS Georeferencer;
- understand Web Mercator tile math;
- manually run Generate XYZ Tiles;
- understand SQLite/MBTiles;
- understand Esri Compact Cache V2.

QGIS still does the rendering. Rasta simply controls the production line.

## What can go into it?

The Factory does not need to understand what the pixels mean. Suitable inputs can include:

- giant city panoramas;
- aerial or satellite imagery;
- drone orthomosaics;
- scanned historical maps or artwork;
- scientific imagery;
- thermal or vegetation products;
- genuinely georeferenced rasters;
- ordinary non-geographic photographs.

If the raster already has real coordinates, Rasta preserves them. If it is merely a flat image, Rasta gives it an explicitly synthetic display location so GIS tiling machinery can manufacture the pyramid.

## What comes out?

**MBTiles** is useful as a general raster tile container for software that understands MBTiles.

**TPKX** packages the same raster pyramid into Esri Compact Cache V2 for compatible Esri viewers such as ArcGIS Earth.

**Both** preserves both forms from the same QGIS-rendered pyramid.

## What Rasta does not do

Rasta cannot invent detail that is absent from the source. A blurry source remains blurry at deep zoom.

Rasta also does not turn a synthetic photograph into real geography. Synthetic placement is merely a deterministic display coordinate system.

The value is not magical enlargement. The value is **manufacturing the existing detail into a form that multiscale viewers can navigate efficiently.**
