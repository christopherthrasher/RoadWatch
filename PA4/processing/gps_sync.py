import csv
import math
from datetime import datetime, timedelta, timezone
from pathlib import Path


class GPSSync:
    def __init__(self, gps_path, video_path):
        self.gps_path = Path(gps_path)
        self.video_path = Path(video_path)
        self.gps_points = self.load_gps()
        self.start_time = self.get_start_time()

    # Load GPS readings from the CSV file
    def load_gps(self):
        gps_points = []

        with self.gps_path.open("r", encoding="utf-8-sig", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                timestamp = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00"))

                latitude = float(row["latitude"])
                longitude = float(row["longitude"])
                accuracy = float(row["horizontalAccuracy"])

                # Skip invalid GPS readings
                if not -90 <= latitude <= 90:
                    continue

                if not -180 <= longitude <= 180:
                    continue

                if not math.isfinite(accuracy) or accuracy < 0:
                    continue

                gps_points.append({
                    "timestamp": timestamp.astimezone(timezone.utc),
                    "latitude": latitude,
                    "longitude": longitude,
                    "gps_accuracy": accuracy
                })

        if not gps_points:
            raise ValueError("No valid GPS readings found.")

        gps_points.sort(key=lambda point: point["timestamp"])

        return gps_points

    # Estimate the recording start time using the video filename
    def get_start_time(self):
        video_id = self.video_path.stem.removeprefix("video_")
        gps_id = self.gps_path.stem.removeprefix("gps_")

        if video_id != gps_id:
            raise ValueError("Video and GPS filenames do not match.")

        local_start = datetime.strptime(video_id, "%Y-%m-%d_%H-%M-%S_%f")

        first_gps_time = self.gps_points[0]["timestamp"]

        # Estimate the UTC offset using the first GPS reading
        difference = first_gps_time.replace(tzinfo=None) - local_start
        offset_hours = round(difference.total_seconds() / 3600)

        start_time = (local_start + timedelta(hours=offset_hours)).replace(tzinfo=timezone.utc)

        # Ensure the GPS recording began near the video start
        delay = (first_gps_time - start_time).total_seconds()

        if abs(delay) > 30:
            raise ValueError("Unable to synchronize recording start time.")

        return start_time

    # Match a video timestamp to the closest GPS reading
    def match_timestamp(self, video_timestamp, max_time_difference=2.0):
        if not math.isfinite(video_timestamp) or video_timestamp < 0:
            raise ValueError("Invalid video timestamp.")

        detection_time = self.start_time + timedelta(seconds=video_timestamp)

        closest_point = min(self.gps_points, key=lambda point: abs((point["timestamp"] - detection_time).total_seconds()))

        time_difference = abs((closest_point["timestamp"] - detection_time).total_seconds())

        # Do not assign a location if no nearby GPS reading exists
        if time_difference > max_time_difference:
            return None

        return {
            "latitude": closest_point["latitude"],
            "longitude": closest_point["longitude"],
            "gps_accuracy": closest_point["gps_accuracy"],
            "timestamp": detection_time.isoformat(),
            "video_timestamp": video_timestamp
        }