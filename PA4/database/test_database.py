
import unittest
import psycopg2


# Check if pothole coordinates are valid
def valid_coordinates(latitude, longitude):
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


class TestDatabase(unittest.TestCase):

    # Integration test: Insert and retrieve a pothole
    def test_insert_and_retrieve(self):
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="roadwatch",
            user="roadwatch",
            password="roadwatch_dev"
        )

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO detections (latitude, longitude, confidence, timestamp)
                VALUES (39.5296, -119.8138, 0.92, '2026-11-04 14:30:00');
            """)

            cursor.execute("""
                SELECT latitude, longitude FROM detections
                WHERE latitude = 39.5296 AND longitude = -119.8138;
            """)

            result = cursor.fetchone()

            self.assertIsNotNone(result)
            self.assertEqual(result[0], 39.5296)
            self.assertEqual(result[1], -119.8138)

        finally:
            conn.rollback()
            conn.close()

    # Unit test: Valid coordinates
    def test_valid_coordinates(self):
        self.assertTrue(valid_coordinates(39.5296, -119.8138))

    # Unit test: Invalid latitude
    def test_invalid_latitude(self):
        self.assertFalse(valid_coordinates(200, -119.8138))

    # Unit test: Invalid longitude
    def test_invalid_longitude(self):
        self.assertFalse(valid_coordinates(39.5296, -200))


if __name__ == "__main__":
    unittest.main()
