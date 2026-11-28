import unittest
from unittest.mock import Mock, patch
from pathlib import Path

from post_processing import PostProcessor


class TestPostProcessor(unittest.TestCase):

    def setUp(self):
        self.gps = Mock()
        self.processor = PostProcessor(self.gps, "images", "v2")

        self.first = {
            "latitude": 36.1,
            "longitude": -115.1,
            "confidence": 0.9,
            "video_timestamp": 1.0
        }

        self.second = {
            "latitude": 36.1,
            "longitude": -115.1,
            "confidence": 0.7,
            "video_timestamp": 2.0
        }

    # Distance calculation tests

    def test_same_location(self):
        distance = self.processor.calculate_distance(self.first, self.second)

        self.assertAlmostEqual(distance, 0.0)

    def test_different_locations(self):
        self.second["latitude"] = 36.101

        distance = self.processor.calculate_distance(self.first, self.second)

        self.assertAlmostEqual(distance, 111.2, delta=0.1)

    # Duplicate removal tests

    def test_remove_duplicate(self):
        result = self.processor.remove_duplicates([self.second, self.first])

        self.assertEqual(result, [self.first])

    def test_keep_distant_detections(self):
        self.second["latitude"] = 36.101

        result = self.processor.remove_duplicates([self.first, self.second])

        self.assertEqual(result, [self.first, self.second])

    def test_keep_different_times(self):
        self.second["video_timestamp"] = 5.0

        result = self.processor.remove_duplicates([self.first, self.second])

        self.assertEqual(result, [self.first, self.second])

    # Image saving test

    def test_save_image(self):
        mock_cv2 = Mock()
        mock_cv2.imwrite.return_value = True
        frame = Mock()

        with patch.dict("sys.modules", {"cv2": mock_cv2}):
            with patch.object(Path, "mkdir"):
                image_path = self.processor.save_image(frame)

        self.assertEqual(Path(image_path).suffix, ".jpg")
        self.assertEqual(Path(image_path).parent, Path("images"))
        mock_cv2.imwrite.assert_called_once_with(image_path, frame)

    # Detection processing tests

    def test_skip_unmatched_detection(self):
        self.gps.match_timestamp.return_value = None

        detections = [{
            "timestamp_sec": 1.0,
            "confidence": 0.9,
            "frame": Mock()
        }]

        with patch.object(self.processor, "save_image") as save_image:
            result = self.processor.process_detections(detections, "recording_1")

        self.assertEqual(result, [])
        save_image.assert_not_called()

    def test_process_valid_detection(self):
        self.gps.match_timestamp.return_value = {
            "latitude": 36.1,
            "longitude": -115.1,
            "gps_accuracy": 2.0,
            "timestamp": "2026-11-24T22:37:17.198000+00:00",
            "video_timestamp": 1.0
        }

        frame = Mock()

        detections = [{
            "timestamp_sec": 1.0,
            "confidence": 0.9,
            "frame": frame
        }]

        with patch.object(self.processor, "save_image", return_value="images/pothole.jpg") as save_image:
            result = self.processor.process_detections(detections, "recording_1")

        expected = [{
            "latitude": 36.1,
            "longitude": -115.1,
            "confidence": 0.9,
            "timestamp": "2026-11-24T22:37:17.198000+00:00",
            "recording_id": "recording_1",
            "video_timestamp": 1.0,
            "image_path": "images/pothole.jpg",
            "model_version": "v2",
            "gps_accuracy": 2.0
        }]

        self.assertEqual(result, expected)
        self.gps.match_timestamp.assert_called_once_with(1.0)
        save_image.assert_called_once_with(frame)


if __name__ == "__main__":
    unittest.main()