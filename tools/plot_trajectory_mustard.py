import os
import glob
import numpy as np
import matplotlib.pyplot as plt

pose_dir = "output_run_demo/poses"
pose_files = sorted(glob.glob(os.path.join(pose_dir, "*.txt")))

print("Number of pose files:", len(pose_files))

translations = []
rotations = []

for f in pose_files:
    T = np.loadtxt(f)

    if T.size != 16:
        print("Skip:", f)
        continue

    T = T.reshape(4, 4)

    R = T[:3, :3]   # rotation
    t = T[:3, 3]    # translation

    rotations.append(R)
    translations.append(t)

translations = np.array(translations)
rotations = np.array(rotations)

print("Translations shape:", translations.shape)
print("Rotations shape:", rotations.shape)

if len(translations) == 0:
    print("No valid poses found!")
    exit()

os.makedirs("output_run_demo/trajectory", exist_ok=True)

x = translations[:, 0]
y = translations[:, 1]
z = translations[:, 2]

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection="3d")

# plot translation trajectory
ax.plot(x, y, z, marker="o", label="Translation trajectory")

# plot local rotation axes every N frames
axis_len = 0.02
step = max(1, len(translations) // 10)

for i in range(0, len(translations), step):
    origin = translations[i]
    R = rotations[i]

    x_axis = R[:, 0] * axis_len
    y_axis = R[:, 1] * axis_len
    z_axis = R[:, 2] * axis_len

    ax.quiver(origin[0], origin[1], origin[2],
              x_axis[0], x_axis[1], x_axis[2],
              length=1, normalize=False)

    ax.quiver(origin[0], origin[1], origin[2],
              y_axis[0], y_axis[1], y_axis[2],
              length=1, normalize=False)

    ax.quiver(origin[0], origin[1], origin[2],
              z_axis[0], z_axis[1], z_axis[2],
              length=1, normalize=False)

ax.set_xlabel("X translation")
ax.set_ylabel("Y translation")
ax.set_zlabel("Z translation")
ax.set_title("3D Trajectory with Rotation Axes")
ax.legend()

plt.savefig("output_run_demo/trajectory/trajectory_3d_with_rotation.png", dpi=300)
plt.close()

print("Saved: output_run_demo/trajectory/trajectory_3d_with_rotation.png")