from pathlib import Path
import cv2
from ultralytics import YOLO

DEFAUT_WEIGHTS = Path(__file__).parent / "weights" / "best.pt"

class PotholeDetector:
    def __init__(self, weights_path: str | Path = DEFAUT_WEIGHTS, conf_thres: float=0.4):
        self.model = YOLO(str(weights_path))
        self.conf_thres = conf_thres

    def detect_video(self, video_path: str | Path, sample_fps: float=3.0) -> list[dict]:
        # Run YOLO on a RouteKeep Cam .mp4 and return detections with exact video timestamps
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Error, could not open video: {video_path}")

        video_fps = cap.get(cv2.CAP_PROP_FPS) or 30.0
        frame_interval = max(1, int(round(video_fps / sample_fps)))

        detections = []
        frame_index = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_index % frame_interval == 0:
                    timestamp_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
                    results = self.model.predict(frame, conf=self.conf_thres, verbose=False)

                    for box in results[0].boxes:
                        detections.append({
                            "timestamp_sec": round(timestamp_sec, 3),
                            "frame_index": frame_index,
                            "confidence": round(float(box.conf), 4),
                            "bbox": [round(coord, 2) for coord in box.xyxy[0].tolist()],
                            "frame": frame.copy(),
                        })

                frame_index += 1

        finally:
            cap.release()

        return detections