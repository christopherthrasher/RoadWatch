-- Developed by the RoadWatch team. No external source code integrated.

CREATE TABLE IF NOT EXISTS detections (
    id SERIAL PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    confidence DOUBLE PRECISION,
    timestamp TIMESTAMP
);
