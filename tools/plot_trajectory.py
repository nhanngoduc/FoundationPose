import os
import glob
import numpy as np
import matplotlib.pyplot as plt

pose_dir = "output_run_demo/poses"
pose_files = sorted(glob.glob(os.path.join(pose_dir, "*.txt")))

print("Number of pose files:", len(pose_files))

translations = []

for f in pose_files:
    try:
        T = np.loadtxt(f)

        if T.size != 16:
            print("Skip:", f)
            continue

        T = T.reshape(4, 4)
        t = T[:3, 3]
        translations.append(t)

    except Exception as e:
        print("Error:", f, e)

translations = np.array(translations)

print("Shape:", translations.shape)

if translations.shape[0] == 0:
    print("No valid poses found!")
    exit()

x = translations[:, 0]
y = translations[:, 1]
z = translations[:, 2]

# 📁 output folder
os.makedirs("output_run_demo/trajectory", exist_ok=True)

# 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
ax.plot(x, y, z, marker="o")
ax.set_title("3D Trajectory")

plt.savefig("output_run_demo/trajectory/trajectory_3d.png")
plt.close()

# time plot
plt.figure()
plt.plot(x, label="x")
plt.plot(y, label="y")
plt.plot(z, label="z")
plt.legend()

plt.savefig("output_run_demo/trajectory/translation_time.png")
plt.close()

print("Saved to output_run_demo/trajectory/")