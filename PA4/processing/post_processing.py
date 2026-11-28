import math
from pathlib import Path
from uuid import uuid4


class PostProcessor:
    def __init__(self, gps_sync, image_dir, model_version):
        self.gps_sync = gps_sync
        self.image_dir = Path(image_dir)
        self.model_version = model_version

    # Calculate the distance between two GPS locations in meters
    def calculate_distance(self, first, second):
        lat1 = math.radians(first["latitude"])
        lat2 = math.radians(second["latitude"])

        delta_lat = lat2 - lat1
        delta_lon = math.radians(second["longitude"] - first["longitude"])

        a = (math.sin(delta_lat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2)

        return 6371000 * 2 * math.asin(math.sqrt(min(1, a)))

    # Reduce repeated detections of the same pothole
    def remove_duplicates(self, detections, distance_threshold=5.0, time_threshold=2.0):
        unique = []

        sorted_detections = sorted(detections, key=lambda detection: detection["confidence"], reverse=True)

        for detection in sorted_detections:
            duplicate = False

            for existing in unique:
                time_difference = abs(detection["video_timestamp"] - existing["video_timestamp"])

                distance = self.calculate_distance(detection, existing)

                if (time_difference <= time_threshold and distance <= distance_threshold):
                    duplicate = True
                    break

            if not duplicate:
                unique.append(detection)

        return sorted(unique, key=lambda detection: detection["video_timestamp"])

    # Save the frame for a pothole detection
    def save_image(self, frame):
        import cv2

        self.image_dir.mkdir(parents=True, exist_ok=True)

        image_path = self.image_dir / f"{uuid4().hex}.jpg"

        if not cv2.imwrite(str(image_path), frame):
            raise IOError("Failed to save detection image.")

        return str(image_path)

    # Convert raw detections into database-ready records
    def process_detections(self, detections, recording_id):
        synchronized = []

        for detection in detections:
            location = self.gps_sync.match_timestamp(detection["timestamp_sec"])

            # Skip detections without a valid GPS match
            if location is None:
                continue

            synchronized.append({**location, "confidence": detection["confidence"], "frame": detection["frame"]})

        unique = self.remove_duplicates(synchronized)

        processed = []

        for detection in unique:
            image_path = self.save_image(detection["frame"])

            processed.append({
                "latitude": detection["latitude"],
                "longitude": detection["longitude"],
                "confidence": detection["confidence"],
                "timestamp": detection["timestamp"],
                "recording_id": recording_id,
                "video_timestamp": detection["video_timestamp"],
                "image_path": image_path,
                "model_version": self.model_version,
                "gps_accuracy": detection["gps_accuracy"]
            })

        return processed