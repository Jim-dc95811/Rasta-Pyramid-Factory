# Rasta Pyramid Factory Roadmap

## Current state

**v0.1.3 TEST remains the current LIVE-PROVEN Rasta baseline for giant-raster manufacturing and ArcGIS Earth display.**

Gigapixel-class proofs remain valid, including London and Barcelona workloads and 20+ minute heartbeat behavior.

---

## New dependency — TPKX converter conformance repair

A 2026-08-20 ArcGIS Field Maps control test proved that the historical MBTiles -> TPKX converter lineage inherited by Rasta is not currently Field Maps-conformant.

Field Maps rejected a project-built TPKX but accepted Esri's official `Usa.tpkx` through the same physical-card/Designer workflow.

### What changes for Rasta

- Rasta's raster inspection, staging, QGIS rendering, MBTiles verification, synthetic placement, and deep-zoom proof remain valid.
- Existing Rasta TPKX evidence remains valid for **ArcGIS Earth**.
- Do **not** claim existing Rasta TPKX is Field Maps-compatible.
- Do **not** rewrite v0.1.3 history.
- After Offline GeoStack's Esri-canonical converter passes Field Maps, integrate that converter into the next Rasta TPKX-capable branch.

Master record:

https://github.com/Jim-dc95811/Offline-GeoStack/blob/main/docs/TPKX_FIELD_MAPS_CONFORMANCE_2026-08-20.md

---

## Converter integration gate

Do not integrate the new converter based on bench tests alone.

Wait for:

```text
small MBTiles
-> ESRI_CANONICAL_TPKX_TEST_v0_2_0
-> small TPKX
-> physical microSD
-> ArcGIS Field Maps PASS
```

Then:

1. import the accepted canonical converter logic into a new Rasta test line;
2. run Rasta regression/self-tests;
3. rerun at least one known city specimen;
4. verify ArcGIS Earth still passes;
5. test a representative Rasta TPKX in Field Maps only if Field Maps is a claimed target for that product.

---

## v0.1.4 TEST — historical separate acceptance boundary

`Rasta_Pyramid_Factory_v0_1_4_TEST` added independent output choices:

```text
TPKX
MBTiles
REST
```

Status remains:

- selection logic: BUILT / SELF-TESTED;
- REST converter branch: BUILT / SELF-TESTED;
- full real-target v0.1.4 acceptance: PENDING;
- REST output: PARKED with Map Fountain.

Do not spend current effort reviving REST while the core TPKX conformance repair is pending upstream.

---

## Core hardening gates

After the canonical converter dependency is resolved, prioritize:

1. cancellation during raster preparation and QGIS rendering;
2. MBTiles-only output on real GUI target;
3. TPKX + MBTiles combination on real GUI target;
4. genuinely georeferenced automatic specimen;
5. very large TIFF/BigTIFF automatic specimen;
6. conservative disk-space preflight;
7. clear source/output byte-count reporting.

---

## Source-screening rule for demonstrations

Before recommending a serious Rasta demo source, verify:

- exact width x height;
- total pixel count;
- daylight / recognizable detail;
- scene density;
- sharpness;
- original-file availability;
- source format/compression;
- reuse rights.

---

## Near-term candidates

- conservative disk-space preflight;
- smarter max-zoom recommendation;
- optional JPEG tiles for photographic sources;
- source pixel/band/compression/georeferencing summary;
- rough output-size warning based on dimensions/tile count;
- controlled BigTIFF, GeoTIFF, historical scan, scientific raster, and drone imagery tests.

---

## Deployment relationship

Rasta remains a manufacturing project.

- **Offline GeoStack** — master manufacturing/integration and current TPKX conformance repair.
- **Rasta** — giant-raster/deep-zoom manufacturing.
- **Map Fountain** — proven router/storage reference; parked.
- **Android Field Maps + ArcGIS Earth** — real Android deployment/acceptance.

---

## Non-goals

- inventing source detail;
- pretending synthetic coordinates are real geography;
- rebuilding QGIS;
- requiring QGIS Desktop operation;
- owning router/mobile delivery architecture;
- calling old Rasta TPKX Field Maps-compatible;
- rewriting v0.1.3 evidence in place;
- reviving REST while parked;
- fake progress percentages.

## Governing rule

> **Rasta manufactures the pyramid. Converter compatibility must be proven on the target before Rasta inherits the claim.**
