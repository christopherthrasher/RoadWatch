# Developed by the RoadWatch team. No external source code integrated.

import unittest
from unittest.mock import Mock
import psycopg2
from database import insert_detection


class TestDatabase(unittest.TestCase):

    # Unit test: Check the database INSERT function
    def test_insert_detection(self):
        mock_cursor = Mock()

        insert_detection(mock_cursor, 39.5296, -119.8138, 0.92, "2026-11-04 14:30:00")

        mock_cursor.execute.assert_called_once_with(
            """
        INSERT INTO detections (latitude, longitude, confidence, timestamp)
        VALUES (%s, %s, %s, %s);
        """,
            (39.5296, -119.8138, 0.92, "2026-11-04 14:30:00")
        )

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


if __name__ == "__main__":
    unittest.main()
