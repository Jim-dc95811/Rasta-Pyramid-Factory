# Rasta Pyramid Factory Roadmap

## Current state

**Automated v0.1.2 architecture: LIVE-PROVEN.**

**v0.1.3 TEST: LIVE-PROVEN** for automatic flat-image manufacture, Atlantic synthetic parking, long-stage heartbeat, verified TPKX publication, and ArcGIS Earth display.

The automated path has crossed gigapixel-class city imagery:

- ✅ 63,000 × 18,589 / ~1.17-billion-pixel London JPEG
- ✅ 62,141 × 14,606 / ~908-million-pixel Barcelona JPEG
- ✅ 20+ minute long-build heartbeat observed live
- ✅ deep-navigation behavior accepted in ArcGIS Earth

## Remaining v0.1.3 hardening gates

1. Test cancellation during raster preparation and QGIS rendering.
2. Test MBTiles-only output directly in the Rasta GUI.
3. Test Both output directly in the Rasta GUI.
4. Exercise at least one genuinely georeferenced raster through AUTO mode.
5. Exercise a very large TIFF/BigTIFF source through the automatic path.
6. Add conservative disk-space preflight before truly enormous staging jobs.

## Source-screening rule for demonstrations

Do not recommend sources by download/file size alone.

Before a source is presented as a serious Rasta demo candidate, verify:

- exact width × height;
- total pixel count;
- daylight / recognizable detail;
- scene density;
- sharpness across the frame;
- original-file availability;
- source format/compression;
- reuse rights.

For visual “hawk dive” demonstrations, dense daylight cityscapes are especially effective because detail is distributed across the frame.

## Near-term release candidates

- automatic conservative disk-space preflight for giant staging rasters and output products;
- smarter automatic max-zoom recommendation based on actual source pixel scale and useful oversampling policy;
- optional JPEG tile output for photographic sources where size matters more than lossless PNG;
- show source pixel type, band count, compression, and georeferencing summary in an Advanced information panel;
- show a rough output-size warning based on pixel dimensions / tile count rather than source megabytes;
- controlled tests with BigTIFF, GeoTIFF mosaics, historical scans, scientific rasters, and drone imagery;
- optional command-line / batch mode after the GUI baseline is accepted.

## Viewer / deployment demonstrations

Rasta is a manufacturing project. It produces native raster pyramids as **MBTiles, TPKX, or Both** and does not own the field delivery hardware.

The current downstream Map Fountain architecture is router-only and has been LIVE-PROVEN on Windows ArcGIS Earth:

```text
Rasta / Factory native TPKX
→ USB SSD
→ GL.iNet Flint 2
→ Samba / SMB
→ private Wi-Fi
→ ArcGIS Earth Windows
```

A production-scale native TPKX remained on the router-attached SSD while ArcGIS Earth opened and rendered it over Wi-Fi.

That proof reinforces Rasta's core design: manufacture clean native products once; do not force the field appliance to understand or rerender them.

**ArcGIS Earth Mobile on the router-only architecture is a Map Fountain acceptance problem, not a Rasta manufacturing problem.**

## Public / community

- Maintain the dedicated `Rasta-Pyramid-Factory` repository as the living technical and plain-language record.
- Keep the canonical Factory / PC / Android router-only flowchart at the top of the repository.
- Preserve the Montreal, Frankfurt, London, Barcelona, and Tower Bridge evidence.
- Publish a short screen recording showing whole-scene → deep-detail navigation.
- Document performance comparison between direct giant-image random access and staged tiled-raster intake.
- Keep the relationship to Offline GeoStack and Map Fountain clear without making Rasta depend on either runtime architecture.

## Non-goals

- inventing source detail;
- pretending synthetic coordinates are real geography;
- rebuilding QGIS;
- requiring QGIS Desktop operation;
- tying Rasta to a single viewer;
- owning router/mobile delivery compatibility;
- rewriting the proven TPKX converter without a verified defect;
- exposing operator choices that automation can make safely;
- displaying fake progress percentages;
- claiming that source file megabytes predict finished pyramid size.
