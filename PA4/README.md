RoadWatch PA4 Prototype


Components

frontend: HTML, CSS, JavaScript

backend: Python, FastAPI

database: PostgreSQL

processing: Python


Detection Data Format

JSON fields: latitude, longitude, confidence, timestamp. PostgreSQL generates the ID.


API Endpoints

POST /detections — saves a detection.GET /detections — retrieves detections.


Docker

Docker Compose will run the components together, with persistent PostgreSQL storage.


Development Goal

Connect all four components using sample data before adding more functionality.


PostgreSQL runs through Docker Compose.

The database table is defined in database/schema.sql. Run this SQL file against the roadwatch database to create the detections table.

The backend connects to PostgreSQL using the service name database and port 5432 inside Docker. Connections from the host computer use localhost:5433.

Database credentials for the local prototype are defined in compose.yaml.
