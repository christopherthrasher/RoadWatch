
import unittest
import subprocess


class TestDatabase(unittest.TestCase):

    def run_sql(self, sql):
        return subprocess.run(
            [
                "docker", "compose", "exec", "-T", "database",
                "psql", "-U", "roadwatch", "-d", "roadwatch",
                "-v", "ON_ERROR_STOP=1", "-t", "-A"
            ],
            input=sql,
            text=True,
            capture_output=True,
            check=True
        ).stdout

    def test_insert_and_retrieve_detection(self):
        sql = """
        BEGIN;
        INSERT INTO detections (latitude, longitude, confidence, timestamp)
        VALUES (39.5296, -119.8138, 0.92, '2026-11-04 14:30:00');

        SELECT latitude, longitude, confidence
        FROM detections
        WHERE latitude = 39.5296 AND longitude = -119.8138;

        ROLLBACK;
        """

        result = self.run_sql(sql)
        self.assertIn("39.5296|-119.8138|0.92", result)

    def test_recording_and_detection_relationship(self):
        sql = """
        BEGIN;

        INSERT INTO recordings (id, video_path, gps_path)
        VALUES ('test_drive', 'videos/test.mp4', 'gps/test.gpx');

        INSERT INTO detections
            (latitude, longitude, confidence, recording_id)
        VALUES (39.5296, -119.8138, 0.92, 'test_drive');

        SELECT recording_id
        FROM detections
        WHERE recording_id = 'test_drive';

        ROLLBACK;
        """

        result = self.run_sql(sql)
        self.assertIn("test_drive", result)

    def test_invalid_recording_id(self):
        sql = """
        BEGIN;

        INSERT INTO detections
            (latitude, longitude, confidence, recording_id)
        VALUES (39.5296, -119.8138, 0.92, 'nonexistent_test_recording');

        ROLLBACK;
        """

        with self.assertRaises(subprocess.CalledProcessError):
            self.run_sql(sql)

    def test_invalid_detection_values(self):
        sql = """
        BEGIN;

        INSERT INTO detections
            (latitude, longitude, confidence)
        VALUES (100, -119.8138, 1.5);

        ROLLBACK;
        """

        with self.assertRaises(subprocess.CalledProcessError):
            self.run_sql(sql)


if __name__ == "__main__":
    unittest.main()
