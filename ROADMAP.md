# Rasta Pyramid Factory Roadmap

## Current state

**Automated v0.1.2 architecture: LIVE-PROVEN.**

**v0.1.3 TEST: LIVE-PROVEN** for automatic flat-image manufacture, Atlantic synthetic parking, verified TPKX publication, and ArcGIS Earth display.

## Remaining v0.1.3 hardening gates

1. Test cancellation during raster preparation and QGIS rendering.
2. Test MBTiles-only output.
3. Test Both output.
4. Exercise at least one genuinely georeferenced raster through AUTO mode.
5. Exercise a very large TIFF/BigTIFF source through the automatic path.
6. Confirm long-stage heartbeat behavior during a deliberately slow run.

## Near-term release candidates

- automatic conservative disk-space preflight for giant staging rasters and output products;
- smarter automatic max-zoom recommendation based on actual source pixel scale and useful oversampling policy;
- optional JPEG tile output for photographic sources where size matters more than lossless PNG;
- show source pixel type, band count, and georeferencing summary in an Advanced information panel;
- controlled tests with BigTIFF, GeoTIFF mosaics, historical scans, scientific rasters, and drone imagery;
- optional command-line / batch mode after the GUI baseline is accepted;
- viewer demonstrations beyond ArcGIS Earth for MBTiles consumers.

## Public / community

- Maintain the dedicated `Rasta-Pyramid-Factory` GitHub repository as the project’s living technical and plain-language record.
- Publish the Montreal overview/deep-zoom evidence pair.
- Publish a short screen recording showing one giant source becoming a multiscale pyramid.
- Document performance comparison between direct giant-PNG random access and staged tiled-raster intake.
- Keep the relationship to Offline GeoStack clear without making either project depend on the other.

## Non-goals

- inventing source detail;
- pretending synthetic coordinates are real geography;
- rebuilding QGIS;
- requiring QGIS Desktop operation;
- tying Rasta to a single viewer;
- rewriting the proven TPKX converter without a verified defect;
- exposing operator choices that automation can make safely;
- displaying fake progress percentages.
