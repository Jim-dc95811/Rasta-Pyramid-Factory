RASTA PYRAMID FACTORY v0.1.3 TEST
SLICE - DICE - PRESENT

PURPOSE
Rasta Pyramid Factory turns giant raster imagery into smooth multiscale raster tile pyramids without requiring the operator to run QGIS Desktop manually.

CURRENT STATUS
- Manual arbitrary-raster pipeline: LIVE-PROVEN.
- Rasta v0.1.2 automated Montreal skyline pipeline: LIVE-PROVEN.
- Rasta v0.1.3 automatic flat-image manufacture + Florida/Atlantic synthetic parking + verified TPKX publication + ArcGIS Earth display: LIVE-PROVEN.

REQUIREMENTS
- Windows 10/11 64-bit
- Python 3.14.5 64-bit
- QGIS 3.44.9 at the normal configured path

NORMAL OPERATOR WORKFLOW
1. Run "Run Rasta Self Test.bat" once after extraction.
2. Launch "Start Rasta Pyramid Factory.bat".
3. CHOOSE IMAGE.
4. Select zoom range if the defaults are not suitable.
5. Select MBTiles, TPKX, or Both.
6. Choose output name/folder.
7. BUILD RASTER PYRAMID.
8. Leave the Factory running until COMPLETE.

AUTOMATIC BEHAVIOR
- Real CRS/geotransform present: preserves real georeferencing.
- Ordinary flat image: creates synthetic projected display placement automatically.
- Flat images are parked near 30N, 80W in the Atlantic east of Florida.
- Giant flat images are decoded once into a temporary tiled working GeoTIFF with overviews before QGIS rendering.
- Original source raster is never modified.

LONG JOBS
v0.1.3 displays a changing heartbeat, elapsed time, stage name, and the most recent meaningful worker message. QGIS percentages are shown only when QGIS actually provides them.

FROZEN RENDERING BASELINE
QGIS 3.44.9
PNG
96 DPI
Antialiasing ON
Metatile 4

TPKX
The included MBTiles_to_TPKX_v0_1_0.py is the frozen proven converter lineage from Offline GeoStack. Do not casually rewrite it.

THIS IS A TEST BUILD
v0.1.3 is LIVE-PROVEN, but release hardening remains open for cancellation, MBTiles-only/Both output, real-georaster AUTO mode, and broader giant-raster coverage.
