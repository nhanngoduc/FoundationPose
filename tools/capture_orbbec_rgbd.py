import os
import time
import cv2
import numpy as np

from pyorbbecsdk import Pipeline, Config, OBSensorType, OBFormat


# =========================
# Output dataset path
# =========================
DATASET_DIR = "/workspace/dataset/mandible"
RGB_DIR = os.path.join(DATASET_DIR, "rgb")
DEPTH_DIR = os.path.join(DATASET_DIR, "depth")

os.makedirs(RGB_DIR, exist_ok=True)
os.makedirs(DEPTH_DIR, exist_ok=True)


# =========================
# Capture settings
# Must match cam_K.txt resolution
# =========================
WIDTH = 640
HEIGHT = 480
FPS = 30

NUM_FRAMES = 100


def main():
    print("Starting Orbbec Femto Bolt RGB-D capture...")
    print(f"Resolution: {WIDTH} x {HEIGHT}, FPS: {FPS}")
    print(f"Saving RGB to:   {RGB_DIR}")
    print(f"Saving depth to: {DEPTH_DIR}")

    pipeline = Pipeline()
    config = Config()

    # -------------------------
    # Enable color stream
    # -------------------------
    color_profiles = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)

    try:
        color_profile = color_profiles.get_video_stream_profile(
            WIDTH, HEIGHT, OBFormat.RGB, FPS
        )
        color_format = "RGB"
        print("Using color format: RGB")
    except Exception:
        color_profile = color_profiles.get_video_stream_profile(
            WIDTH, HEIGHT, OBFormat.MJPG, FPS
        )
        color_format = "MJPG"
        print("RGB not available, using color format: MJPG")

    config.enable_stream(color_profile)

    # -------------------------
    # Enable depth stream
    # -------------------------
    depth_profiles = pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)

    try:
        depth_profile = depth_profiles.get_video_stream_profile(
            WIDTH, HEIGHT, OBFormat.Y16, FPS
        )
        print("Using depth format: Y16")
    except Exception:
        depth_profile = depth_profiles.get_default_video_stream_profile()
        print("Y16 not available, using default depth profile")

    config.enable_stream(depth_profile)

    pipeline.start(config)
    print("Pipeline started.")

    saved_count = 0

    try:
        # Warm-up frames
        print("Warming up camera...")
        for _ in range(30):
            pipeline.wait_for_frames(100)

        print("Start capturing...")

        while saved_count < NUM_FRAMES:
            frames = pipeline.wait_for_frames(100)

            if frames is None:
                print("No frames received.")
                continue

            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            if color_frame is None or depth_frame is None:
                print("Missing color or depth frame.")
                continue

            # -------------------------
            # Convert color frame
            # -------------------------
            color_data = np.frombuffer(color_frame.get_data(), dtype=np.uint8)

            if color_format == "RGB":
                color = color_data.reshape((HEIGHT, WIDTH, 3))
                color_bgr = cv2.cvtColor(color, cv2.COLOR_RGB2BGR)

            elif color_format == "MJPG":
                color_bgr = cv2.imdecode(color_data, cv2.IMREAD_COLOR)
                if color_bgr is None:
                    print("Failed to decode MJPG color frame.")
                    continue
                color_bgr = cv2.resize(color_bgr, (WIDTH, HEIGHT))

            else:
                print("Unsupported color format.")
                continue

            # -------------------------
            # Convert depth frame
            # -------------------------
            depth_data = np.frombuffer(depth_frame.get_data(), dtype=np.uint16)
            depth_raw = depth_data.reshape((HEIGHT, WIDTH))

            # Save depth as 16-bit PNG in millimeters,
            # following the sample RGB-D dataset style.
            #
            # Important:
            # When loading this depth for FoundationPose,
            # convert it to meters:
            # depth_m = depth_raw.astype(np.float32) / 1000.0
            depth_mm = depth_raw.astype(np.uint16)

            # -------------------------
            # Save files with matched names
            # -------------------------
            name = f"{saved_count:06d}"

            rgb_path = os.path.join(RGB_DIR, f"{name}.png")
            depth_path = os.path.join(DEPTH_DIR, f"{name}.png")

            cv2.imwrite(rgb_path, color_bgr)
            cv2.imwrite(depth_path, depth_mm)

            print(f"Saved frame {name}:")
            print(f"  RGB:   {rgb_path}")
            print(f"  Depth: {depth_path}")
            print(f"  Depth min/max raw: {depth_mm.min()} / {depth_mm.max()}")

            saved_count += 1
            time.sleep(0.03)

    finally:
        pipeline.stop()
        print("Pipeline stopped.")

    print(f"Done. Saved {saved_count} RGB-D frames.")


if __name__ == "__main__":
    main()