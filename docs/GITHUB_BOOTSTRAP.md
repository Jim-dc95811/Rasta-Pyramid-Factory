# GitHub Bootstrap

Repository:

`Jim-dc95811/Rasta-Pyramid-Factory`

About description:

> Turn giant raster imagery into smooth multiscale tiled products. Slice. Dice. Present.

Recommended topics:

- `qgis`
- `gdal`
- `raster`
- `mbtiles`
- `tpkx`
- `tile-pyramid`
- `gigapixel`
- `deep-zoom`
- `geospatial`
- `python`
- `offline`
- `image-processing`

## One-time exact-source materialization history — 2026-08-16

The initial repository population used a temporary GitHub Actions workflow named `Materialize exact source` to work around a connector size ceiling while preserving the exact large Python source files.

### Run #1 — FAILED

The first payload staging attempt successfully verified/materialized `RASTA_PIPELINE.py` but encountered a corrupted compressed converter payload before the commit step.

A delayed GitHub email can therefore still say:

`Materialize exact source: All jobs have failed`

That notification is historical and does **not** describe the final repository state.

### Run #2 — SUCCESS

The corrected run:

- decompressed the staged source payloads;
- verified exact expected byte sizes / SHA-256 values;
- committed the normal source files;
- removed the temporary payload directory;
- removed the temporary workflow itself.

Final GitHub file sizes:

- `RASTA_PIPELINE.py` — **26,050 bytes**
- `MBTiles_to_TPKX_v0_1_0.py` — **21,318 bytes**

The repository does not depend on that workflow for normal operation.

## Maintainer rule

Do not recreate or re-run the historical materializer merely because an old failed-run notification appears. Verify the current repository source files and current Actions state first.
