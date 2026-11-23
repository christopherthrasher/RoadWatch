
CREATE TABLE IF NOT EXISTS recordings (
    id TEXT PRIMARY KEY,
    video_path TEXT NOT NULL,
    gps_path TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'completed', 'failed'))
);

CREATE TABLE IF NOT EXISTS detections (
    id SERIAL PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL
        CHECK (latitude BETWEEN -90 AND 90),
    longitude DOUBLE PRECISION NOT NULL
        CHECK (longitude BETWEEN -180 AND 180),
    confidence DOUBLE PRECISION
        CHECK (confidence BETWEEN 0 AND 1),
    timestamp TIMESTAMP,
    recording_id TEXT,
    video_timestamp DOUBLE PRECISION
        CHECK (video_timestamp >= 0),
    image_path TEXT,
    model_version TEXT,
    gps_accuracy DOUBLE PRECISION
        CHECK (gps_accuracy >= 0),

    FOREIGN KEY (recording_id) REFERENCES recordings(id)
);
