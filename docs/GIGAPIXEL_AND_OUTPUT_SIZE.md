# Gigapixel proof + output-size guidance

## The human experience

Rasta is useful because a true raster pyramid preserves visual continuity across scale.

A large photograph can be viewed as one continuous visual space:

```text
whole scene
→ district / structure
→ block / building
→ vehicles / windows / people-sized detail
```

The operator does not pick resolution layers. The viewer requests progressively finer raster tiles as the operator moves through the pyramid.

A useful plain-language description from live testing is:

> **See the whole scene like a hawk. Dive into any detail that catches your eye.**

The detail is not created by Rasta. It was already present in the source pixels; the pyramid makes it practical to navigate.

## First gigapixel-class automated proof — Kings Reach Panorama 2

**Status: LIVE-PROVEN — 2026-08-16**

Source:

- `Kings_reach_panorama_2.jpg`
- **63,000 × 18,589 pixels**
- approximately **1.17 billion source pixels**
- ordinary non-geographic JPEG

Rasta v0.1.3 result:

- **67,619 final raster tiles**
- **Z0–Z18**
- **30 Compact Cache V2 bundles**
- elapsed: **0:23:07**
- Windows File Explorer TPKX size: **1,949,149 KB**
- ArcGIS Earth: **PASS**

The wide view presents London as a conventional city panorama. Deep navigation toward the London Eye resolves individual people inside the observation pods. That is the intended multiscale effect: information that is effectively invisible in the overview becomes readable when the operator dives into that part of the source.

## Barcelona / Tibidabo distributed-detail proof

**Status: LIVE-PROVEN — 2026-08-16**

Source:

- `Tibidabo.jpg`
- **62,141 × 14,606 pixels**
- approximately **908 million source pixels**
- ordinary non-geographic JPEG

Rasta v0.1.3 result:

- **52,482 final raster tiles**
- **Z0–Z18**
- **30 Compact Cache V2 bundles**
- elapsed: **0:20:40**
- ArcGIS Earth: **PASS**

This source demonstrated a particularly strong visual-navigation effect because useful detail is distributed across nearly the entire city. The operator can move from whole-city context into individual buildings, rooftops, cars, parking areas, construction equipment, balconies, trees, and road geometry in many different directions.

## Tower Bridge proof

**Status: LIVE-PROVEN — 2026-08-16**

Source:

- `Tower_Bridge_from_Shad_Thames.jpg`
- **15,287 × 7,643 pixels**
- ordinary non-geographic JPEG

Rasta v0.1.3 result:

- **6,976 tiles**
- **Z0–Z18**
- **22 bundles**
- elapsed: **0:02:18**
- Windows File Explorer TPKX size: **294,910 KB**
- ArcGIS Earth: **PASS**

The operator could move from the full Tower Bridge scene into small river/shore details without manually changing image layers.

## Source file size is not the main predictor

Do **not** estimate Rasta output size from the source file size alone.

The source file is a compressed container. The stronger predictors are:

1. **pixel dimensions / total pixel count**;
2. **requested pyramid zoom range**;
3. **scene complexity / compressibility**;
4. **tile encoding**.

A heavily compressed JPEG can contain hundreds of millions or more than a billion pixels while occupying less disk space than a much lower-resolution TIFF.

Example from live testing:

- Kings Reach Panorama 2 was roughly a 100 MB-class JPEG but contained about **1.17 billion pixels** and produced a **1,949,149 KB** TPKX.
- A roughly 288 MB Pittsburgh TIFF inspected at only **8,688 × 5,792 pixels** — about 50 million pixels — despite being a much larger source file on disk.

Therefore:

> **Do not judge a source image by how many megabytes the file weighs. Judge it by what pixels are actually inside.**

## Better Rasta source screening

For an impressive deep-navigation demonstration, verify these before downloading or recommending a source:

- exact width × height;
- total pixel count;
- daylight / recognizable visual detail;
- scene density;
- focus/sharpness across the frame;
- source format and compression;
- actual original-file availability;
- reuse rights.

For city-panorama demonstrations, high-value content includes buildings, roads, vehicles, bridges, boats, windows, signs, rooftop equipment, construction activity, and other recognizable detail spread across the frame.

## Current output format note

Rasta currently manufactures PNG raster tiles in the proven baseline. Photographic JPEG sources can therefore expand substantially when transformed from one highly compressed monolithic file into thousands of independently addressable lossless raster tiles across many pyramid levels.

That storage increase buys a different optimization target:

> **The source file is optimized for carrying a photograph. The pyramid is optimized for navigating through it.**
