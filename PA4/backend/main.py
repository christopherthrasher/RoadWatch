from fastapi import FastAPI

from database import get_connection

from models import DetectionCreate

app = FastAPI(title="RoadWatch API")


@app.get("/detections")
def get_detections(recording_id: str | None = None):
    query = """
        SELECT id, latitude, longitude, confidence, timestamp, recording_id
        FROM detections
    """
    params = ()

    if recording_id is not None:
        query += " WHERE recording_id = %s"
        params = (recording_id,)

    query += " ORDER BY id DESC"

    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


@app.post("/detections", status_code=201)
def create_detection(detection: DetectionCreate):
    with get_connection() as conn:
        return conn.execute(
            """
            INSERT INTO detections
                (latitude, longitude, confidence, timestamp, recording_id)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, latitude, longitude, confidence, timestamp, recording_id
            """,
            (
                detection.latitude,
                detection.longitude,
                detection.confidence,
                detection.timestamp,
                detection.recording_id,
            ),
        ).fetchone()