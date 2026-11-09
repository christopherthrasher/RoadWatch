
import unittest
import psycopg2


class TestDatabase(unittest.TestCase):

    def test_insert_and_retrieve(self):
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host="localhost",
            port=5433,
            database="roadwatch",
            user="roadwatch",
            password="roadwatch_dev"
        )

        cursor = conn.cursor()

        # Insert a test pothole
        cursor.execute("""
            INSERT INTO detections (latitude, longitude, confidence, timestamp)
            VALUES (39.5296, -119.8138, 0.92, '2026-11-04 14:30:00');
        """)

        # Retrieve the test pothole
        cursor.execute("""
            SELECT latitude, longitude FROM detections
            WHERE latitude = 39.5296 AND longitude = -119.8138;
        """)

        # Gets the first matching row from SELECT
        result = cursor.fetchone()

        # Check that the coordinates match
        self.assertEqual(result[0], 39.5296)
        self.assertEqual(result[1], -119.8138)

        # Undo the insert so the database stays clean
        conn.rollback()
        cursor.close()
        conn.close()


if __name__ == "__main__":
    unittest.main()
