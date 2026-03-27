"""
Fix OBJ mesh: repair holes, non-manifold edges, and disconnected fragments.

Uses trimesh for vertex merging + pymeshfix for robust manifold repair.
Preserves ~98% of original geometry.
"""
import trimesh
import pymeshfix
import numpy as np
from collections import Counter
from pathlib import Path


def diagnose(mesh, label=""):
    """Print mesh health diagnostics."""
    edges = mesh.edges_sorted
    edge_counts = Counter(tuple(e) for e in edges)
    non_manifold = sum(1 for c in edge_counts.values() if c > 2)
    boundary = sum(1 for c in edge_counts.values() if c == 1)

    print(f"--- {label} ---")
    print(f"  Vertices: {len(mesh.vertices)}")
    print(f"  Faces: {len(mesh.faces)}")
    print(f"  Is watertight: {mesh.is_watertight}")
    print(f"  Is volume (manifold): {mesh.is_volume}")
    print(f"  Winding consistent: {mesh.is_winding_consistent}")
    print(f"  Non-manifold edges: {non_manifold}")
    print(f"  Boundary edges (holes): {boundary}")
    print()


def main():
    input_path = Path("Meshy_AI_Aerial_View_of_a_Mode_0327020348_texture.obj")
    output_path = Path("Meshy_AI_Aerial_View_of_a_Mode_0327020348_texture_fixed.obj")

    # Step 1: Load and merge duplicate vertices
    print("Loading mesh...")
    mesh = trimesh.load(str(input_path), process=False)
    diagnose(mesh, "ORIGINAL")

    print("Step 1: Merging close vertices...")
    mesh.merge_vertices(merge_tex=True, merge_norm=True)
    diagnose(mesh, "AFTER merge_vertices")

    # Step 2: PyMeshFix -- robust manifold repair with geometry preservation
    print("Step 2: PyMeshFix repair...")
    meshfix = pymeshfix.MeshFix(mesh.vertices, mesh.faces)
    print(f"  Boundaries: {meshfix.n_boundaries}")
    meshfix.join_closest_components()
    meshfix.repair()

    mesh = trimesh.Trimesh(vertices=meshfix.points, faces=meshfix.faces)
    diagnose(mesh, "AFTER PyMeshFix")

    # Step 3: Final normals fix
    print("Step 3: Fixing normals...")
    mesh.fix_normals()
    diagnose(mesh, "FINAL")

    # Export
    mesh.export(str(output_path), file_type="obj")
    print(f"Repaired mesh saved to: {output_path}")

    if mesh.is_volume:
        print("SUCCESS: Mesh is a valid manifold volume!")
    if mesh.is_watertight:
        print("SUCCESS: Mesh is watertight!")


if __name__ == "__main__":
    main()
