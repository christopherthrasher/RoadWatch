import unittest
from unittest.mock import patch, mock_open
from datetime import datetime, timezone
from pathlib import Path

from gps_sync import GPSSync


class TestGPSSync(unittest.TestCase):

    def setUp(self):
        self.gps = GPSSync.__new__(GPSSync)
        self.gps.gps_path = Path("gps_2026-11-24_14-37-16_198.csv")
        self.gps.video_path = Path("video_2026-11-24_14-37-16_198.mov")

        self.gps.start_time = datetime(2026, 11, 24, 22, 37, 16, 198000, tzinfo=timezone.utc)

        self.gps.gps_points = [
            {
                "timestamp": datetime(
                    2026, 11, 24, 22, 37, 17, 198000,
                    tzinfo=timezone.utc
                ),
                "latitude": 36.1,
                "longitude": -115.1,
                "gps_accuracy": 2.0
            },
            {
                "timestamp": datetime(
                    2026, 11, 24, 22, 37, 18, 198000,
                    tzinfo=timezone.utc
                ),
                "latitude": 36.2,
                "longitude": -115.2,
                "gps_accuracy": 3.0
            }
        ]

        self.csv_header = "timestamp,latitude,longitude,horizontalAccuracy\n"

    # GPS loading tests

    def test_load_valid_gps(self):
        data = self.csv_header + ("2026-11-24T22:37:17.198Z,36.1,-115.1,2.0\n")

        with patch.object(Path, "open", mock_open(read_data=data)):
            points = self.gps.load_gps()

        self.assertEqual(points, [self.gps.gps_points[0]])

    def test_load_invalid_gps(self):
        data = self.csv_header + ("2026-11-24T22:37:17.198Z,91,-115.1,2.0\n")

        with patch.object(Path, "open", mock_open(read_data=data)):
            with self.assertRaises(ValueError):
                self.gps.load_gps()

    # Recording start time tests

    def test_get_start_time(self):
        self.assertEqual(self.gps.get_start_time(), self.gps.start_time)

    def test_mismatched_files(self):
        self.gps.video_path = Path("video_different_recording.mov")

        with self.assertRaises(ValueError):
            self.gps.get_start_time()

    # GPS matching tests

    def test_match_closest_timestamp(self):
        result = self.gps.match_timestamp(1.8)

        self.assertEqual(result["latitude"], 36.2)
        self.assertEqual(result["longitude"], -115.2)
        self.assertEqual(result["gps_accuracy"], 3.0)
        self.assertEqual(result["video_timestamp"], 1.8)
        self.assertEqual(result["timestamp"], "2026-11-24T22:37:17.998000+00:00")

    def test_match_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            self.gps.match_timestamp(-1.0)

    def test_match_time_boundary(self):
        result = self.gps.match_timestamp(4.0)

        self.assertIsNotNone(result)
        self.assertEqual(result["latitude"], 36.2)

    def test_match_outside_time_boundary(self):
        result = self.gps.match_timestamp(4.001)

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()