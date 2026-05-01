import trimesh
import numpy as np
from pathlib import Path

in_path = Path("dataset/mandible/mesh/IOS trios LowerJawScan.ply")  # đổi thành .stl nếu cần
out_path = Path("dataset/mandible/mesh/mandible.obj")

mesh = trimesh.load(in_path, force="mesh")

# nếu scan đang là mm thì đổi sang meter
mesh.vertices = mesh.vertices / 1000.0

# center mesh
mesh.vertices = mesh.vertices - mesh.vertices.mean(axis=0)

# clean nhẹ
mesh.remove_duplicate_faces()
mesh.remove_degenerate_faces()
mesh.remove_unreferenced_vertices()

mesh.export(out_path)

print("Saved:", out_path)
print("Vertices:", mesh.vertices.shape)
print("Faces:", mesh.faces.shape)
print("Bounds:", mesh.bounds)
print("Size:", mesh.bounds[1] - mesh.bounds[0])