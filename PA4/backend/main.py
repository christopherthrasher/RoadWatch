from fastapi import FastAPI

from database import get_connection

from models import DetectionCreate

app = FastAPI(title="RoadWatch API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/detections")
def get_detections():
    with get_connection() as conn:
        detections = conn.execute(
            """
            SELECT id, latitude, longitude, confidence, timestamp
            FROM detections
            ORDER BY id DESC
            """
        ).fetchall()

    return detections

@app.post("/detections", status_code=201)
def create_detection(detection: DetectionCreate):
    with get_connection() as conn:
        saved_detection = conn.execute(
            """
            INSERT INTO detections
                (latitude, longitude, confidence, timestamp)
            VALUES (%s, %s, %s, %s)
            RETURNING id, latitude, longitude, confidence, timestamp
            """,
            (
                detection.latitude,
                detection.longitude,
                detection.confidence,
                detection.timestamp,
            ),
        ).fetchone()

    return saved_detection