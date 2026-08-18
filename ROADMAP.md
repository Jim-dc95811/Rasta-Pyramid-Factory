# Rasta Pyramid Factory Roadmap

## Current state

**v0.1.3 TEST is the current LIVE-PROVEN baseline.**

It is live-proven for automatic flat-image manufacture, Atlantic synthetic parking, long-stage heartbeat, verified TPKX publication, and ArcGIS Earth display across multiple large city-image workloads.

Gigapixel-class proofs include:

- ✅ 63,000 × 18,589 / ~1.17-billion-pixel London JPEG
- ✅ 62,141 × 14,606 / ~908-million-pixel Barcelona JPEG
- ✅ 20+ minute long-build heartbeat observed live
- ✅ deep-navigation behavior accepted in ArcGIS Earth

---

## v0.1.4 TEST — separate acceptance boundary

`Rasta_Pyramid_Factory_v0_1_4_TEST` was built from the v0.1.3 live-proven core.

It changed output selection to three independent choices:

```text
TPKX
MBTiles
REST
```

Any one, any two, or all three may be selected.

Status:

- selection logic: **BUILT / SELF-TESTED**;
- REST converter branch: **BUILT / SELF-TESTED**;
- real end-to-end v0.1.4 Factory acceptance: **PENDING**;
- REST output on real intended mobile target: **PENDING**.

The REST branch came from the Map Fountain / Static REST WMTS exploration. Do not let that experimental downstream output redefine Rasta's core mission.

---

## Core hardening gates

Prioritize work that strengthens Rasta as a general raster-pyramid factory:

1. cancellation during raster preparation and QGIS rendering;
2. MBTiles-only output on the real GUI target;
3. TPKX + MBTiles combination on the real GUI target;
4. at least one genuinely georeferenced raster through the automatic path;
5. very large TIFF/BigTIFF automatic specimen;
6. conservative disk-space preflight before truly enormous staging jobs;
7. clear source/output byte-count reporting.

REST-specific work stays lower priority unless a real deployment path reopens the need.

---

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

For visual “hawk dive” demonstrations, dense daylight cityscapes are especially effective because useful detail is distributed across the frame.

---

## Near-term Rasta candidates

- conservative disk-space preflight for giant staging rasters and output products;
- smarter max-zoom recommendation based on actual source pixel scale and useful oversampling policy;
- optional JPEG tile output for photographic sources where size matters more than lossless PNG;
- source pixel type / band count / compression / georeferencing summary in an Advanced information panel;
- rough output-size warning based on pixel dimensions / tile count rather than source megabytes;
- controlled tests with BigTIFF, GeoTIFF mosaics, historical scans, scientific rasters, and drone imagery;
- optional command-line / batch mode only after the GUI baseline is accepted.

---

## Deployment relationship

Rasta is a manufacturing project. It should not own field-delivery hardware.

The project family now separates roles:

- **Offline GeoStack** — master TPKX/map-manufacturing and field-mapping architecture.
- **Map Fountain** — live-proven router/storage experiments, now parked from the primary personal-phone path.
- **Android Field Maps + ArcGIS Earth** — current personal-phone / microSD deployment.
- **Rasta** — giant-raster/deep-zoom pyramid manufacturing.

### SD-card opportunity

If a field user's card has spare capacity, Rasta products can provide useful deep-zoom cityscapes, historical maps, specialty scans, or other single-raster reference material.

That is a downstream use, not a reason to change Rasta's manufacturing core.

---

## Public / community

- maintain the dedicated `Rasta-Pyramid-Factory` repository as the living technical and plain-language record;
- keep v0.1.3 LIVE-PROVEN status distinct from v0.1.4 SELF-TESTED status;
- preserve Montreal, Frankfurt, London, Barcelona, and Tower Bridge evidence;
- publish a short screen recording showing whole-scene → deep-detail navigation;
- document performance comparison between direct giant-image random access and staged tiled-raster intake;
- keep the relationship to Offline GeoStack, Map Fountain, and Android deployment clear without making Rasta depend on any runtime architecture.

---

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
- claiming source file megabytes predict finished pyramid size;
- treating the v0.1.4 REST experiment as live-proven before the target passes it.

## Governing rule

> **Rasta manufactures the pyramid. Deployment belongs downstream.**
