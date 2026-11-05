
import unittest
import subprocess


class TestDatabase(unittest.TestCase):

    def test_insert_and_retrieve(self):
        sql = """
        BEGIN;
        INSERT INTO detections (latitude, longitude, confidence, timestamp)
        VALUES (39.5296, -119.8138, 0.92, '2026-11-04 14:30:00');

        SELECT latitude, longitude, confidence
        FROM detections
        WHERE latitude = 39.5296 AND longitude = -119.8138;

        ROLLBACK;
        """

        result = subprocess.run(
            ["docker", "compose", "exec", "-T", "database",
             "psql", "-U", "roadwatch", "-d", "roadwatch",
             "-v", "ON_ERROR_STOP=1"],
            input=sql,
            text=True,
            capture_output=True,
            check=True
        )

        self.assertIn("39.5296", result.stdout)
        self.assertIn("-119.8138", result.stdout)


if __name__ == "__main__":
    unittest.main()
