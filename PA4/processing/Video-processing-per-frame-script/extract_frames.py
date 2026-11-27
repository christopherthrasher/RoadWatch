"""
   Mines candidate pothole frames (including false positives like puddles or curbs
   reflectors) and clean background frames from raw phone or dashcam videos so they
   can be labeled in Roboflow for model fine-tuning.
"""

import argparse
from pathlib import Path
import random
import cv2
from ultralytics import YOLO

VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv"}

def extract_frames(weights: str, video_dir: Path, out_dir: Path, conf: float, bg_rate: float):
    # Load the baseline (or previously fine-tuned) YOLO weights
    model = YOLO(weights)

    # Create the output directory if it doesn't already exist
    out_dir.mkdir(parents=True, exist_ok=True)

    # Collect all supported video files in alphabetical order
    videos = sorted(p for p in video_dir.iterdir() if p.suffix.lower() in VIDEO_EXTS)
    if not videos:
        print(f"No videos found in {video_dir}")
        return

    for video_path in videos:
        cap = cv2.VideoCapture(str(video_path))

        # Fall back to 30 FPS if video metadata doesn't report a valid frame rate
        fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        # Sample 1 fram per second to avoid saving near-identical consecutive frames
        interval = max(1, int(round(fps)))
        frame_ind = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            # Only run inference on the sampled frames
            if frame_ind % interval == 0:
                # Use a low confidence threshold to catch both weak pothole detections
                # and false positives (hard negatives) for Roboflow cleanup
                results = model.predict(frame, conf=conf, verbose= False)
                has_detection = len(results[0].boxes) > 0

                # Save every fram with a detection, plus a small random sample of
                # clean road frames to teach the model what "no pothole" looks like
                if has_detection or random.random() < bg_rate:
                    tag = 'det' if has_detection else 'bg'
                    out_path = out_dir / f"{video_path.stem}_f{frame_ind}_{tag}.jpg"
                    cv2.imwrite(str(out_path), frame)

            frame_ind += 1

        cap.release()

    print(f"Done! Saved {len(list(out_dir.glob('*.jpg')))} frames to {out_dir}")

if __name__ == "__main__":
    # Parse CLI arguments so the script can be reused across different video batches
    parser = argparse.ArgumentParser(
        description="Extract candidate pothole and backfround frames for Roboflow"
    )
    parser.add_argument("--weights", required=True, help="Path to best.pt model weights")
    parser.add_argument("--input", required=True, help="Folder containing raw training videos")
    parser.add_argument("--output", required=True, help="Folder to save extracted .jpg frames")
    parser.add_argument(
        "--conf",
        type=float,
        default=0.20,
        help="Confidence threshold for candidate mining (default: 0.20)",
    )
    parser.add_argument(
        "--bg_rate",
        type=float,
        default=0.05,
        help="Fraction of clean frames to save as background (default: 0.05)",
    )
    args = parser.parse_args()

    extract_frames(args.weights, Path(args.input), Path(args.output), args.conf, args.bg_rate)