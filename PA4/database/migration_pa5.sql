
BEGIN;

-- Create the recordings table.
CREATE TABLE IF NOT EXISTS recordings (
    id TEXT PRIMARY KEY,
    video_path TEXT NOT NULL,
    gps_path TEXT NOT NULL,
    uploaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'processing', 'completed', 'failed'))
);

-- Add the new detection columns.
ALTER TABLE detections
    ADD COLUMN IF NOT EXISTS recording_id TEXT,
    ADD COLUMN IF NOT EXISTS video_timestamp DOUBLE PRECISION,
    ADD COLUMN IF NOT EXISTS image_path TEXT,
    ADD COLUMN IF NOT EXISTS model_version TEXT,
    ADD COLUMN IF NOT EXISTS gps_accuracy DOUBLE PRECISION;

-- Add validation rules and the foreign key.
ALTER TABLE detections
    ADD CONSTRAINT detections_latitude_check
        CHECK (latitude BETWEEN -90 AND 90),
    ADD CONSTRAINT detections_longitude_check
        CHECK (longitude BETWEEN -180 AND 180),
    ADD CONSTRAINT detections_confidence_check
        CHECK (confidence BETWEEN 0 AND 1),
    ADD CONSTRAINT detections_video_timestamp_check
        CHECK (video_timestamp >= 0),
    ADD CONSTRAINT detections_gps_accuracy_check
        CHECK (gps_accuracy >= 0),
    ADD CONSTRAINT detections_recording_id_fkey
        FOREIGN KEY (recording_id) REFERENCES recordings(id);

COMMIT;
