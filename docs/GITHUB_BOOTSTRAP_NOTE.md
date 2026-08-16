# GitHub bootstrap note

The initial Rasta repository population used a **temporary one-time GitHub Actions workflow** named `Materialize exact source` to work around a connector size ceiling while preserving the exact large Python source files.

## Run history — 2026-08-16

### Run #1

**Result: FAILED**

The first payload staging attempt successfully verified/materialized `RASTA_PIPELINE.py` but encountered a corrupted compressed converter payload before the commit step.

This run can still generate delayed GitHub email such as:

`Materialize exact source: All jobs have failed`

That notification is historical and does **not** describe the final repository state.

### Run #2

**Result: SUCCESS**

The corrected run:

- decompressed the staged source payloads;
- verified the expected exact byte sizes and SHA-256 values;
- committed `RASTA_PIPELINE.py` and `MBTiles_to_TPKX_v0_1_0.py` into the normal repository tree;
- removed the temporary payload directory;
- removed the temporary materialization workflow itself.

Final materialized file sizes recorded by GitHub:

- `RASTA_PIPELINE.py` — **26,050 bytes**
- `MBTiles_to_TPKX_v0_1_0.py` — **21,318 bytes**

The repository therefore does not depend on that workflow for normal operation.

## Maintainer rule

Do not re-run or recreate the historical materializer merely because an old failed-run email appears. Verify the current repository files and current Actions state first.
