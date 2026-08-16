from pathlib import Path
import hashlib
from RASTA_PIPELINE import synthetic_bounds, estimate_synthetic_tiles, recommended_max_zoom, _parse_json_payload, overview_factors, web_mercator_from_lonlat, load_config, synthetic_bounds_for_config

HERE = Path(__file__).resolve().parent
errors=[]
b=synthetic_bounds(20634,10317,1.0)
if b != (-10317.0,10317.0,-5158.5,5158.5): errors.append(f"bounds mismatch: {b}")
count=estimate_synthetic_tiles(b,0,18)
if count != 12489: errors.append(f"manual-proof tile count mismatch: {count}")
if recommended_max_zoom(1.0) != 18: errors.append("recommended max zoom mismatch")

# Regression: GDAL JSON may be followed by a codec/GDAL diagnostic. v0.1.0
# concatenated streams and json.loads() raised "Extra data". The parser must
# recover the first complete JSON object without losing raster dimensions.
probe = '{"size":[29684,7620],"driverShortName":"PNG"}\nWarning 1: harmless trailing diagnostic\n'
try:
    parsed = _parse_json_payload(probe)
    if parsed.get("size") != [29684, 7620]: errors.append(f"GDAL JSON parser regression: {parsed}")
except Exception as exc:
    errors.append(f"GDAL JSON parser raised on trailing diagnostic: {exc}")

# Performance regression: giant flat rasters must be staged into a tiled GeoTIFF
# with power-of-two overviews instead of leaving QGIS to random-read a PNG/JPEG.
factors = overview_factors(29684, 7620)
if factors != [2, 4, 8, 16, 32, 64, 128]: errors.append(f"overview plan mismatch: {factors}")

# v0.1.3 regression: flat images park at a deterministic synthetic anchor
# east of Florida instead of at lon/lat 0,0 off Africa.
cfg = load_config(HERE)
cx, cy = web_mercator_from_lonlat(cfg.synthetic_anchor_lon, cfg.synthetic_anchor_lat)
if abs(cfg.synthetic_anchor_lon - (-80.0)) > 1e-9 or abs(cfg.synthetic_anchor_lat - 30.0) > 1e-9:
    errors.append(f"synthetic parking anchor mismatch: {cfg.synthetic_anchor_lon}, {cfg.synthetic_anchor_lat}")
fb = synthetic_bounds_for_config(cfg, 29684, 7620, 1.0)
if abs(((fb[0]+fb[1])/2)-cx) > 0.01 or abs(((fb[2]+fb[3])/2)-cy) > 0.01:
    errors.append(f"Florida parking center mismatch: {fb}")

conv=HERE/'MBTiles_to_TPKX_v0_1_0.py'
sha=hashlib.sha256(conv.read_bytes()).hexdigest()
expected='7e685b396bf2a6a5ca89fdb710b2ae2e25f8e66014e9162408f166b01d78fc97'
if sha != expected: errors.append(f"frozen converter hash mismatch: {sha}")
if errors:
    print('RASTA SELF TEST: FAIL')
    for e in errors: print(' -',e)
    raise SystemExit(1)
print('RASTA SELF TEST: PASS')
print('Manual proof synthetic bounds:', b)
print('Manual proof Z0-Z18 tile addresses:', f'{count:,}')
print('1 m/pixel recommended max zoom:', recommended_max_zoom(1.0))
print('29,684 px working overview factors:', factors)
print('Synthetic parking anchor:', f'{cfg.synthetic_anchor_lat:.1f}N {abs(cfg.synthetic_anchor_lon):.1f}W')
print('Frozen converter SHA-256:', sha)
