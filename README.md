# B'nai Emunah Synagogue — 3D Massing Model

<video src="output/3d-model-demo.mp4" autoplay loop muted playsinline width="100%"></video>

## Overview

This project generates a 3D `.OBJ` massing model of Congregation B'nai Emunah (Tulsa, OK) from OpenStreetMap data, for use in a preservation project.

## Files

| File | Description |
|------|-------------|
| `bnai_emunah_massing.py` | Python script — reads JSON, writes `.OBJ` |
| `bnai_emunah.json` | Overpass API JSON data (building outline) |
| `bnai_emunah_massing.obj` | Generated 3D model (Wavefront OBJ) |

## Model Output

- **OSM Way ID:** 251539920
- **Building name:** B'nai Emunah
- **Tags:** `amenity=place_of_worship`, `building=yes`, `religion=jewish`
- **Outline vertices:** 38 unique points
- **OBJ vertices:** 76 (38 base + 38 roofline at 12m height)
- **OBJ faces:** 110 (38 wall quads + 36 roof triangles + 36 bottom triangles)
- **Coordinate origin:** 36.1375°N, 95.9762°W (center of building)
- **Extruded height:** 12.0m (~40 ft)

## API Fix

### Problem: Empty results from `overpass.osm.ch`

The original script used the Swiss Overpass mirror (`overpass.osm.ch`). All queries returned empty `"elements": []` regardless of search parameters. The server's timestamp field showed `"112709"` instead of a real ISO date — indicating a broken or stale database.

Additionally, the original query used `"name"="Congregation B'nai Emunah"` which doesn't match the actual OSM tag value `"B'nai Emunah"`.

### Solution

1. **Switched API endpoint** from `https://overpass.osm.ch/api/interpreter` to `https://overpass-api.de/api/interpreter` (the main Overpass server).
2. **Added `-L` flag** to curl to follow HTTP redirects (the main server redirects POST requests).
3. **Used regex name match** `"name"~"B.nai Emunah",i` to handle the apostrophe and case variations.
4. **Used `out geom`** format which embeds lat/lon geometry directly in the response, eliminating the need for a separate node-resolution pass.

### Working curl command

```bash
curl -sL -X POST \
  -d 'data=[out:json];nwr["name"~"B.nai Emunah",i](36.12,-96.00,36.16,-95.95);out geom;' \
  https://overpass-api.de/api/interpreter -o bnai_emunah.json
```

## Script Rewrite

The original script required manual XML pasting into a string literal and parsed XML with `ElementTree`. The rewritten version:

- **Reads a JSON file** (`bnai_emunah.json`) instead of embedded XML
- **Accepts command-line argument** for input file path (defaults to `bnai_emunah.json` in script directory)
- **Handles closed-way duplicate nodes** — OSM closed ways repeat the first node as the last; the duplicate is stripped to avoid degenerate faces
- **Wraps wall loop correctly** — uses modular indexing `(i+1) % num` so the last wall connects back to the first vertex
- **Adds bottom faces** — reversed winding order for correct downward normals, making the model watertight
- **Parses height tags safely** — catches `ValueError`/`TypeError` on non-numeric `height` or `building:levels` values
- **Uses object names from OSM tags** — `o B'nai Emunah` instead of `o building_0`
- **Writes output next to the script** — not relative to the shell's working directory

## Usage

```bash
# Fetch fresh data (optional — bnai_emunah.json is already included)
curl -sL -X POST \
  -d 'data=[out:json];nwr["name"~"B.nai Emunah",i](36.12,-96.00,36.16,-95.95);out geom;' \
  https://overpass-api.de/api/interpreter -o bnai_emunah.json

# Generate the OBJ model
python3 bnai_emunah_massing.py

# Or specify a different input file
python3 bnai_emunah_massing.py /path/to/other_data.json
```

The output `bnai_emunah_massing.obj` can be imported into Blender, SketchUp, Rhino, or any 3D software that supports Wavefront OBJ.
