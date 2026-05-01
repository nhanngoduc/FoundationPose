import os
import trimesh

mesh_path = "/workspace/dataset/mandible/mesh/mandible.obj"

print("Current working directory:", os.getcwd())
print("Mesh path:", mesh_path)
print("File exists:", os.path.exists(mesh_path))

if not os.path.exists(mesh_path):
    raise FileNotFoundError(f"Mesh file not found: {mesh_path}")

mesh = trimesh.load(mesh_path, force="mesh")

print("Mesh loaded successfully!")
print("Vertices:", len(mesh.vertices))
print("Faces:", len(mesh.faces))
print("Bounds:")
print(mesh.bounds)
print("Extents:", mesh.extents)