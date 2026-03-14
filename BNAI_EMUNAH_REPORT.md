# B'nai Emunah Synagogue - 3D Massing Model Report

**Project:** Congregation B'nai Emunah Preservation Project
**Location:** 1719 S Owasso Ave, Tulsa, OK 74120
**Coordinates:** 36.1374°N, 95.9764°W
**Date:** March 14, 2026

---

## Executive Summary

This report documents five different approaches used to generate and visualize a 3D massing model of the B'nai Emunah Synagogue in Tulsa, Oklahoma. The project utilized OpenStreetMap data and various tools to create accurate architectural representations for preservation purposes.

---

## Data Source

**OpenStreetMap Way ID:** [251539920](https://www.openstreetmap.org/way/251539920)

### Building Information
- **Name:** B'nai Emunah
- **Type:** Place of Worship (Jewish Synagogue)
- **Amenity:** place_of_worship
- **Religion:** Jewish
- **Building:** Yes
- **Geometry:** 38 nodes defining the building footprint

### Coordinates Bounds
- **Min Latitude:** 36.1371270
- **Max Latitude:** 36.1379026
- **Min Longitude:** -95.9766613
- **Max Longitude:** -95.9758051

---

## Approach 1: Python Script with Bevel and Smoothing

### Method
Custom Python script ([bnai_emunah_massing.py](bnai_emunah_massing.py)) that generates a 3D OBJ file from Overpass API JSON data.

### Technical Details
- **Script Language:** Python 3
- **Input:** [bnai_emunah.json](bnai_emunah.json) (Overpass API data)
- **Output:** [bnai_emunah_massing.obj](bnai_emunah_massing.obj)
- **Origin Point:** (36.1375°, -95.9762°)
- **Default Height:** 12.0 meters (~40 feet for sanctuary)

### Features
- GPS to local meter coordinate conversion using WGS84 Earth radius
- Automatic height extraction from OSM tags (`height` or `building:levels`)
- Generates extruded building mass with:
  - Wall faces (quad strips connecting base to top)
  - Roof face (fan triangulation)
  - Ground face (reverse-wound fan triangulation)
- Removes duplicate closing nodes from OSM closed ways
- Handles multiple building parts if present

### Code Highlights
```python
# Coordinate conversion
R = 6378137  # Earth Radius in meters
x = (math.radians(lon) - math.radians(origin_lon)) * math.cos(math.radians(origin_lat)) * R
y = (math.radians(lat) - math.radians(origin_lat)) * R

# Height determination
height = DEFAULT_HEIGHT
if 'height' in tags:
    height = float(tags['height'])
elif 'building:levels' in tags:
    height = float(tags['building:levels']) * 3.5
```

### Output Characteristics
- Beveling and smoothing applied for realistic appearance
- Clean OBJ format compatible with all major 3D software
- Vertex indices start at 1 (OBJ standard)
- Proper face winding for correct normals

### Results
- **Status:** ✅ Successful
- **Files Generated:** `bnai_emunah_massing.obj`
- **Image:** [Attached - Python output with beveling]

---

## Approach 2: Blender with GIS Addon

### Method
Import and visualization using Blender's GIS (Geographic Information System) addon.

### Technical Details
- **Software:** Blender (version with BlenderGIS addon)
- **Addon:** BlenderGIS / OSM importer
- **Data Source:** OpenStreetMap direct import

### Features
- Native OSM data import
- Automatic georeferencing
- Real-world scale accuracy
- Professional rendering capabilities
- Material and lighting setup

### Results
- **Status:** ✅ Best Output
- **Quality:** Highest visual fidelity
- **Image:** [Attached - Blender GIS render]
- **Notes:** This approach produced the most polished and professional-looking output with proper materials, lighting, and rendering quality.

---

## Approach 3: OpenStreetMap Web View

### Method
Direct visualization using OpenStreetMap's web interface.

### Access
**URL:** [https://www.openstreetmap.org/way/251539920#map=19/36.137431/-95.976485&layers=P](https://www.openstreetmap.org/way/251539920#map=19/36.137431/-95.976485&layers=P)

### Technical Details
- **View Level:** Zoom 19 (maximum detail)
- **Layers:** P (Parking/POI layer enabled)
- **Center:** 36.137431°N, 95.976485°W

### Features
- 2D top-down view
- Shows building footprint accurately
- Displays surrounding context (streets, parking, neighboring buildings)
- Community-maintained data
- Real-time updates from OSM contributors

### Results
- **Status:** ✅ Successful
- **View Type:** 2D orthographic
- **Image:** [Attached - OpenStreetMap screenshot]
- **Use Case:** Best for verifying footprint accuracy and spatial context

---

## Approach 4: Google Maps Satellite View

### Method
Google Maps satellite imagery and 3D view.

### Access
**URL:** [Google Maps Link](https://www.google.com/maps/place/The+Synagogue+%7C+Congregation+B'nai+Emunah/@36.1374021,-95.9766479,152m/data=!3m1!1e3!4m14!1m7!3m6!1s0x87b6ec98ec66f64d:0xa566155ef6176f09!2sThe+Synagogue+%7C+Congregation+B'nai+Emunah!8m2!3d36.1376435!4d-95.9764804!16s%2Fg%2F1tfqg9r6!3m5!1s0x87b6ec98ec66f64d:0xa566155ef6176f09!8m2!3d36.1376435!4d-95.9764804!16s%2Fg%2F1tfqg9r6?entry=ttu&g_ep=EgoyMDI2MDMxMS4wIKXMDSoASAFQAw%3D%3D)

### Technical Details
- **Place ID:** ChIJTW9m7JjstocRCW8X9l4VZqU
- **Coordinates:** 36.1376435°N, 95.9764804°W
- **Altitude:** 152m view height
- **View Mode:** Satellite with 3D

### Features
- High-resolution aerial photography
- 3D building models (where available)
- Street View integration
- Business information (The Synagogue | Congregation B'nai Emunah)
- Reviews and photos from visitors

### Results
- **Status:** ✅ Successful
- **View Types:** Satellite, 3D, Street View
- **Image:** [Attached - Google Maps screenshot]
- **Use Case:** Best for real-world reference imagery and roof details

---

## Approach 5: F4Map 3D Visualization

### Method
Interactive 3D visualization using F4Map's OpenStreetMap-based renderer.

### Access
**URL:** [https://demo.f4map.com/#lat=36.1374515&lon=-95.9762206&zoom=19&camera.theta=64.996&camera.phi=-29.507](https://demo.f4map.com/#lat=36.1374515&lon=-95.9762206&zoom=19&camera.theta=64.996&camera.phi=-29.507)

### Technical Details
- **Platform:** F4Map (OSM 3D renderer)
- **Coordinates:** 36.1374515°N, 95.9762206°W
- **Zoom Level:** 19
- **Camera Theta:** 64.996° (vertical angle)
- **Camera Phi:** -29.507° (horizontal rotation)

### Features
- Real-time 3D rendering from OSM data
- Interactive camera controls
- Shows building heights and extrusions
- Displays surrounding buildings in 3D context
- Trees, roads, and urban features
- WebGL-based rendering

### Results
- **Status:** ✅ Successful
- **View Type:** Interactive 3D perspective
- **Image:** [Attached - F4Map screenshot]
- **Use Case:** Best for interactive exploration and urban context visualization

---

## Comparison Matrix

| Approach | Type | Quality | Interactivity | Context | Accuracy | Best For |
|----------|------|---------|---------------|---------|----------|----------|
| **1. Python Script** | 3D Model | Good | None (file) | No | High | Modeling pipeline, CAD import |
| **2. Blender GIS** | 3D Render | Excellent | Full (Blender) | Yes | High | Presentation, visualization |
| **3. OpenStreetMap** | 2D Map | Good | Limited (pan/zoom) | Excellent | Very High | Footprint verification |
| **4. Google Maps** | Satellite/3D | Very Good | Moderate | Good | High | Real-world reference |
| **5. F4Map** | 3D Web | Good | Excellent | Excellent | High | Quick 3D preview, sharing |

---

## Technical Files

### Generated Files
1. **[bnai_emunah.json](bnai_emunah.json)** - Overpass API response with building geometry
2. **[bnai_emunah_massing.obj](bnai_emunah_massing.obj)** - 3D mesh file (OBJ format)
3. **[bnai_emunah_massing.py](bnai_emunah_massing.py)** - Python generator script

### Data Retrieval Command
```bash
curl -sL -X POST \
  -d 'data=[out:json];nwr["name"~"B.nai Emunah",i](36.12,-96.00,36.16,-95.95);out geom;' \
  https://overpass-api.de/api/interpreter -o bnai_emunah.json
```

---

## Recommendations

### Best Output: Approach 2 (Blender GIS)
The Blender GIS approach produced the highest quality visualization with proper materials, lighting, and rendering capabilities. Recommended for:
- Final presentations
- Preservation documentation
- Stakeholder reviews
- Publication-quality images

### Best for Development: Approach 1 (Python Script)
The Python script provides the most flexibility and can be:
- Integrated into automated pipelines
- Modified for different buildings
- Extended with additional features
- Used in CAD/BIM workflows

### Best for Verification: Approach 3 (OpenStreetMap)
The OSM web view is ideal for:
- Verifying footprint accuracy
- Understanding site context
- Checking data quality
- Community collaboration

### Best for Reference: Approach 4 (Google Maps)
Google Maps satellite imagery provides:
- Real-world photographic reference
- Roof details and textures
- Seasonal vegetation
- Parking and site features

### Best for Quick Preview: Approach 5 (F4Map)
F4Map offers:
- Instant 3D visualization
- Easy sharing via URL
- No software installation
- Urban context at a glance

---

## Future Enhancements

### Potential Improvements
1. **Texture Mapping:** Add photorealistic textures from satellite imagery
2. **Interior Modeling:** Extend to include interior spaces
3. **LOD Generation:** Create multiple Levels of Detail for performance
4. **Animation:** Create walkthrough or flyover animations
5. **VR/AR Export:** Generate formats for immersive viewing
6. **Documentation:** Link architectural drawings and historical photos

### Data Enrichment
- Survey data integration for precise measurements
- Historical records for temporal accuracy
- Architectural details (windows, doors, ornaments)
- Material specifications
- Structural elements

---

## Project Metadata

- **Script Version:** 1.0
- **Python Requirements:** Python 3.x, json, math, os, sys (stdlib only)
- **OBJ Format Version:** Wavefront OBJ (universal)
- **Coordinate System:** WGS84 (EPSG:4326) → Local Cartesian
- **Data License:** OpenStreetMap ODbL (Open Database License)
- **Last Updated:** March 14, 2026

---

## Conclusion

All five approaches successfully generated or visualized the B'nai Emunah Synagogue building in 3D or detailed 2D formats. The Blender GIS approach (#2) delivered the best visual output, while the Python script (#1) provides the most flexibility for integration into preservation workflows. The combination of these approaches provides comprehensive documentation suitable for architectural preservation, community engagement, and historical records.

The variety of methods demonstrates the accessibility of geospatial data and 3D modeling tools for heritage conservation projects, enabling multiple stakeholders to engage with the building's digital representation in ways appropriate to their needs and technical capabilities.

---

*Report generated for the Congregation B'nai Emunah Preservation Project*
*Based on OpenStreetMap data and multiple visualization approaches*
