import os
import trimesh
import matplotlib.pyplot as plt
import numpy as np


# =========================
# 1. Mesh path
# =========================
mesh_path = "/workspace/dataset/mandible/mesh/mandible.obj"

print("Current working directory:", os.getcwd())
print("Mesh path:", mesh_path)
print("File exists:", os.path.exists(mesh_path))

if not os.path.exists(mesh_path):
    raise FileNotFoundError(f"Mesh file not found: {mesh_path}")


# =========================
# 2. Load mesh
# =========================
mesh = trimesh.load(mesh_path, force="mesh")

print("\nMesh loaded successfully!")
print("Vertices:", len(mesh.vertices))
print("Faces:", len(mesh.faces))
print("Bounds:")
print(mesh.bounds)
print("Extents:", mesh.extents)
print("Centroid:", mesh.centroid)

v = mesh.vertices


# =========================
# 3. Sample vertices for plotting
# =========================
max_points = 30000

if len(v) > max_points:
    idx = np.random.choice(len(v), max_points, replace=False)
    vv = v[idx]
else:
    vv = v


# =========================
# 4. Save 2D orientation views
# =========================
fig = plt.figure(figsize=(15, 5))

views_2d = [
    ("Front view: X-Z", 0, 2),
    ("Top view: X-Y", 0, 1),
    ("Side view: Y-Z", 1, 2),
]

axis_names = ["X", "Y", "Z"]

for i, (title, ax1, ax2) in enumerate(views_2d):
    ax = fig.add_subplot(1, 3, i + 1)

    ax.scatter(vv[:, ax1], vv[:, ax2], s=0.2)
    ax.set_title(title)
    ax.set_xlabel(axis_names[ax1])
    ax.set_ylabel(axis_names[ax2])
    ax.axis("equal")
    ax.grid(True)

plt.tight_layout()

out_2d = "/workspace/dataset/mandible/mesh/orientation_check_2d.png"
plt.savefig(out_2d, dpi=300)
plt.close()

print("\nSaved 2D orientation image to:")
print(out_2d)


# =========================
# 5. Save 3D orientation view
# =========================
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection="3d")

ax.scatter(vv[:, 0], vv[:, 1], vv[:, 2], s=0.15)

length = max(mesh.extents) * 0.6
origin = mesh.centroid

# X axis
ax.quiver(origin[0], origin[1], origin[2], length, 0, 0, linewidth=2)
ax.text(origin[0] + length, origin[1], origin[2], "X", fontsize=14)

# Y axis
ax.quiver(origin[0], origin[1], origin[2], 0, length, 0, linewidth=2)
ax.text(origin[0], origin[1] + length, origin[2], "Y", fontsize=14)

# Z axis
ax.quiver(origin[0], origin[1], origin[2], 0, 0, length, linewidth=2)
ax.text(origin[0], origin[1], origin[2] + length, "Z", fontsize=14)

ax.set_title("3D Mandible Orientation with XYZ Axes")
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

max_range = np.array([
    vv[:, 0].max() - vv[:, 0].min(),
    vv[:, 1].max() - vv[:, 1].min(),
    vv[:, 2].max() - vv[:, 2].min(),
]).max() / 2.0

mid_x = (vv[:, 0].max() + vv[:, 0].min()) * 0.5
mid_y = (vv[:, 1].max() + vv[:, 1].min()) * 0.5
mid_z = (vv[:, 2].max() + vv[:, 2].min()) * 0.5

ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

ax.view_init(elev=25, azim=45)

out_3d = "/workspace/dataset/mandible/mesh/orientation_check_3d.png"
plt.savefig(out_3d, dpi=300)
plt.close()

print("\nSaved 3D orientation image to:")
print(out_3d)


# =========================
# 6. Save 6 canonical views
# =========================
fig = plt.figure(figsize=(18, 12))

# (title, elev, azim)
views_6 = [
    ("+X view",   0,   0),
    ("-X view",   0, 180),
    ("+Y view",   0,  90),
    ("-Y view",   0, -90),
    ("+Z view",  90, -90),
    ("-Z view", -90, -90),
]

for i, (title, elev, azim) in enumerate(views_6):
    ax = fig.add_subplot(2, 3, i + 1, projection="3d")
    ax.scatter(vv[:, 0], vv[:, 1], vv[:, 2], s=0.15)

    # Draw short XYZ axes
    axis_len = max(mesh.extents) * 0.35

    ax.quiver(origin[0], origin[1], origin[2], axis_len, 0, 0, linewidth=1.5)
    ax.quiver(origin[0], origin[1], origin[2], 0, axis_len, 0, linewidth=1.5)
    ax.quiver(origin[0], origin[1], origin[2], 0, 0, axis_len, linewidth=1.5)

    ax.text(origin[0] + axis_len, origin[1], origin[2], "X", fontsize=10)
    ax.text(origin[0], origin[1] + axis_len, origin[2], "Y", fontsize=10)
    ax.text(origin[0], origin[1], origin[2] + axis_len, "Z", fontsize=10)

    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    ax.view_init(elev=elev, azim=azim)

plt.tight_layout()

out_6views = "/workspace/dataset/mandible/mesh/orientation_check_6views.png"
plt.savefig(out_6views, dpi=300)
plt.close()

print("\nSaved 6-view orientation image to:")
print(out_6views)

print("\nDone.")