import json
import math
import os
import sys

# ==========================================
# Generates a 3D .OBJ massing model from Overpass API JSON data.
#
# Usage:
#   python bnai_emunah_massing.py [input.json]
#
# If no argument given, reads bnai_emunah.json from the same directory.
# To fetch data:
#   curl -sL -X POST \
#     -d 'data=[out:json];nwr["name"~"B.nai Emunah",i](36.12,-96.00,36.16,-95.95);out geom;' \
#     https://overpass-api.de/api/interpreter -o bnai_emunah.json
# ==========================================

FILENAME = "bnai_emunah_massing.obj"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LAT_ORIGIN = 36.1375
LON_ORIGIN = -95.9762
DEFAULT_HEIGHT = 12.0  # Approx 40ft (Sanctuary height)


def latlon_to_meters(lat, lon, origin_lat, origin_lon):
    """Converts GPS coordinates to local meters for 3D software."""
    R = 6378137  # Earth Radius in meters
    x = (math.radians(lon) - math.radians(origin_lon)) * math.cos(math.radians(origin_lat)) * R
    y = (math.radians(lat) - math.radians(origin_lat)) * R
    return x, y


def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)


def generate_obj(json_path):
    try:
        data = load_json(json_path)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {json_path}")
        return
    except json.JSONDecodeError as e:
        print(f"❌ Error: Malformed JSON in {json_path}: {e}")
        return

    elements = data.get('elements', [])
    ways = [e for e in elements if e.get('type') == 'way' and 'geometry' in e]

    if not ways:
        print("⚠️  No ways with geometry found in JSON. Generating a placeholder box instead.")
        create_placeholder()
        return

    obj_path = os.path.join(SCRIPT_DIR, FILENAME)
    with open(obj_path, 'w') as f:
        f.write("# B'nai Emunah Synagogue Massing Model\n")
        f.write("# Generated for Preservation Project\n\n")
        vert_offset = 1  # OBJ vertex indices are 1-based

        for way_idx, way in enumerate(ways):
            geom = way['geometry']
            way_nodes = [(pt['lat'], pt['lon']) for pt in geom]

            if len(way_nodes) < 3:
                continue

            # Remove duplicate closing node (OSM closed ways repeat the first node)
            if way_nodes[0] == way_nodes[-1]:
                way_nodes = way_nodes[:-1]

            if len(way_nodes) < 3:
                continue

            # Determine height from tags
            tags = way.get('tags', {})
            height = DEFAULT_HEIGHT
            try:
                if 'height' in tags:
                    height = float(tags['height'])
                elif 'building:levels' in tags:
                    height = float(tags['building:levels']) * 3.5
            except (ValueError, TypeError):
                pass

            name = tags.get('name', f'building_{way_idx}')
            num = len(way_nodes)
            f.write(f"o {name}\n")

            # Write vertices: pairs of (base, top) for each node
            for lat, lon in way_nodes:
                x, y = latlon_to_meters(lat, lon, LAT_ORIGIN, LON_ORIGIN)
                f.write(f"v {x:.6f} 0 {y:.6f}\n")
                f.write(f"v {x:.6f} {height:.6f} {y:.6f}\n")

            # Wall faces (quads connecting consecutive node pairs, wrapping around)
            for i in range(num):
                j = (i + 1) % num
                b1 = vert_offset + i * 2      # base of current node
                t1 = vert_offset + i * 2 + 1  # top of current node
                b2 = vert_offset + j * 2      # base of next node
                t2 = vert_offset + j * 2 + 1  # top of next node
                f.write(f"f {b1} {t1} {t2} {b2}\n")

            # Roof face (fan triangulation from first top vertex)
            top0 = vert_offset + 1
            for i in range(1, num - 1):
                ti = vert_offset + i * 2 + 1
                ti1 = vert_offset + (i + 1) * 2 + 1
                f.write(f"f {top0} {ti} {ti1}\n")

            # Bottom face (fan triangulation, reversed winding for downward normal)
            bot0 = vert_offset
            for i in range(1, num - 1):
                bi = vert_offset + i * 2
                bi1 = vert_offset + (i + 1) * 2
                f.write(f"f {bot0} {bi1} {bi}\n")

            vert_offset += num * 2

    print(f"🎉 Success! 3D Model saved to: {obj_path}")


def create_placeholder():
    obj_path = os.path.join(SCRIPT_DIR, FILENAME)
    with open(obj_path, 'w') as f:
        f.write("# Placeholder Box (40m x 30m x 12m)\n")
        f.write("v -20 0 -15\nv -20 12 -15\n")   # 1,2  front-left
        f.write("v 20 0 -15\nv 20 12 -15\n")      # 3,4  front-right
        f.write("v 20 0 15\nv 20 12 15\n")         # 5,6  back-right
        f.write("v -20 0 15\nv -20 12 15\n")       # 7,8  back-left
        f.write("f 1 2 4 3\n")   # front wall
        f.write("f 3 4 6 5\n")   # right wall
        f.write("f 5 6 8 7\n")   # back wall
        f.write("f 7 8 2 1\n")   # left wall
        f.write("f 2 8 6 4\n")   # roof
        f.write("f 1 3 5 7\n")   # bottom
    print(f"✅ Placeholder model created: {obj_path}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_json = os.path.join(script_dir, "bnai_emunah.json")
    json_path = sys.argv[1] if len(sys.argv) > 1 else default_json
    generate_obj(json_path)
