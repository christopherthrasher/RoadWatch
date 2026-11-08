# RoadWatch Backend

Python/FastAPI API for storing and retrieving detections in PostgreSQL.

## Run with Docker

Start Docker Desktop. From the PA4 directory, run:

```bash
docker compose up -d --build backend
```

API: http://localhost:8000
Interactive API documentation: http://localhost:8000/docs

After changing backend code, rerun the build command above.

## Endpoints

- GET /health — confirms the API server is responding.
- POST /detections — saves a detection and returns it with its generated ID.
- GET /detections — returns saved detections, newest ID first.

GET /health does not check database connectivity.

## Example POST /detections body

```json
{
  "latitude": 39.5296,
  "longitude": -119.8138,
  "confidence": 0.94,
  "timestamp": "2026-11-08T20:00:00"
}
```

All four fields are required. Latitude must be between -90 and 90,
and longitude between -180 and 180. PostgreSQL generates the ID.

Successful submissions return 201. Invalid input returns 422.
Confidence is currently a numeric value without an enforced range.
We have to decide on confidence units and a timestamp timezone convention.

## Connecting other components

- Programs running on the same computer: http://localhost:8000
- Processing containers in the same Compose project: http://backend:8000

Processing should submit detections through the API.

Browser frontend integration may require CORS configuration for
the frontend's origin; this is not configured yet.

## Database settings

The backend reads DB_HOST, DB_PORT, DB_NAME, DB_USER, and DB_PASSWORD.

Docker Compose sets the database address to database:5432.
Local Python development defaults to localhost:5433.

Database records are stored in the existing postgres_data volume.
Test records are local data and are not included in Git commits.

## Troubleshooting

View backend logs from PA4:

```bash
docker compose logs backend
```

If port 5433 is occupied, check for a local PostgreSQL service.
If port 8000 is occupied, stop any locally running Uvicorn server.
