
# RoadWatch Database

This folder contains the PostgreSQL database schema, migration script, and integration tests for the RoadWatch project.

## Files

- `schema.sql` - Creates the database tables for new installations.
- `migration_pa5.sql` - Updates an existing PA4 database to the PA5 schema.
- `test_database.py` - Contains four integration tests for database functionality.

## Database Tables

### recordings

Stores information about uploaded roadway recordings.

- `id` - Unique recording ID.
- `video_path` - Path to the uploaded video file.
- `gps_path` - Path to the GPS file.
- `uploaded_at` - Time the recording was added.
- `status` - Processing status: pending, processing, completed, or failed.

### detections

Stores potholes identified from recordings.

- `id` - Unique detection ID.
- `latitude`, `longitude` - GPS coordinates.
- `confidence` - Detection confidence from 0 to 1.
- `timestamp` - Time of the detection.
- `recording_id` - References the associated recording.
- `video_timestamp` - Detection time in seconds from the start of the video.
- `image_path` - Path to a representative pothole image.
- `model_version` - Version of the detection model.
- `gps_accuracy` - GPS accuracy value, when available.

Each recording can have multiple detections. Video files, GPS files, and images are stored outside PostgreSQL, with their paths saved in the database.

## Database Setup

Run these commands from the `PA4` folder.

Start PostgreSQL:

```powershell
docker compose up -d database
```

For a new database, Docker automatically runs `schema.sql` during initialization.

For an existing PA4 database, apply the migration:

```powershell
Get-Content .\database\migration_pa5.sql -Raw | docker compose exec -T database psql -U roadwatch -d roadwatch -v ON_ERROR_STOP=1
```

The migration preserves existing detection records and can be rerun without duplicating the new columns or constraints.

## Running Tests

With PostgreSQL running, execute:

```powershell
python -m unittest discover -s database -p "test_database.py" -v
```

The four integration tests verify:

1. Inserting and retrieving a detection.
2. Connecting a detection to an existing recording.
3. Rejecting a detection with an invalid recording ID.
4. Rejecting invalid detection values.

All four tests passed during PA5 database testing.

## Notes

- The database runs through Docker Compose.
- PostgreSQL uses port 5433 on the host and port 5432 inside Docker.
- Existing PA4 detections remain supported because `recording_id` is optional.
- The backend and processing components will need to use the new fields as PA5 functionality is implemented.
