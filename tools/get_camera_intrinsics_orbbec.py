# Script này mục tiêu là:

# Orbbec Femto Bolt
# → lấy fx, fy, cx, cy từ SDK
# → tạo ma trận K
# → lưu vào /workspace/dataset/mandible/cam_K.txt


# cam_K.txt sẽ có dạng:

# fx 0  cx
# 0  fy cy
# 0  0  1

import os
import numpy as np

from pyorbbecsdk import Pipeline, Config, OBSensorType, OBFormat


OUT_PATH = "/workspace/dataset/mandible/cam_K.txt"

# Resolution phải giống resolution bạn sẽ dùng để capture RGB-D
WIDTH = 640
HEIGHT = 480
FPS = 30


def get_value(obj, names):
    for name in names:
        if hasattr(obj, name):
            return getattr(obj, name)
    raise AttributeError(f"Cannot find any of {names} in object: {dir(obj)}")


def save_K_from_intrinsic(intrinsic, out_path):
    fx = get_value(intrinsic, ["fx"])
    fy = get_value(intrinsic, ["fy"])

    # Orbbec SDK/version khác nhau có thể dùng cx/cy hoặc ppx/ppy
    cx = get_value(intrinsic, ["cx", "ppx"])
    cy = get_value(intrinsic, ["cy", "ppy"])

    K = np.array([
        [fx, 0.0, cx],
        [0.0, fy, cy],
        [0.0, 0.0, 1.0]
    ], dtype=np.float32)

    print("\nIntrinsic values:")
    print("fx:", fx)
    print("fy:", fy)
    print("cx:", cx)
    print("cy:", cy)

    print("\nCamera matrix K:")
    print(K)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    np.savetxt(out_path, K, fmt="%.8f")

    print("\nSaved cam_K.txt to:")
    print(out_path)


def main():
    print("Starting Orbbec Femto Bolt pipeline...")

    pipeline = Pipeline()
    config = Config()

    # Lấy color stream profile
    color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)

    try:
        color_profile = color_profiles.get_video_stream_profile(
            WIDTH, HEIGHT, OBFormat.RGB, FPS
        )
        print(f"Using COLOR profile: {WIDTH}x{HEIGHT}, RGB, {FPS} FPS")
    except Exception:
        print("RGB format not available, trying MJPG...")
        color_profile = color_profiles.get_video_stream_profile(
            WIDTH, HEIGHT, OBFormat.MJPG, FPS
        )
        print(f"Using COLOR profile: {WIDTH}x{HEIGHT}, MJPG, {FPS} FPS")

    config.enable_stream(color_profile)

    profile = pipeline.start(config)

    try:
        print("Pipeline started.")

        cam_param = pipeline.get_camera_param()

        print("\nCamera parameter object:")
        print(cam_param)

        if hasattr(cam_param, "rgb_intrinsic"):
            intrinsic = cam_param.rgb_intrinsic
            print("\nUsing cam_param.rgb_intrinsic")
        elif hasattr(cam_param, "color_intrinsic"):
            intrinsic = cam_param.color_intrinsic
            print("\nUsing cam_param.color_intrinsic")
        else:
            print("\nAvailable fields in cam_param:")
            print(dir(cam_param))
            raise AttributeError(
                "Cannot find rgb_intrinsic / color_intrinsic in camera parameter object"
            )

        save_K_from_intrinsic(intrinsic, OUT_PATH)

    finally:
        pipeline.stop()
        print("\nPipeline stopped.")


if __name__ == "__main__":
    main()