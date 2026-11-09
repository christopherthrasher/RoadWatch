import unittest
from pydantic import ValidationError
from models import DetectionCreate


class TestBackend(unittest.TestCase):

    def test_invalid_latitude(self):
        with self.assertRaises(ValidationError):
            DetectionCreate(
                latitude=200,
                longitude=-119.8138,
                confidence=0.92,
                timestamp="2026-11-08T20:00:00"
            )


if __name__ == "__main__":
    unittest.main()
