RoadWatch PA4 Prototype


Components

frontend: HTML, CSS, JavaScript

backend: Python, FastAPI

database: PostgreSQL

processing: Python


Detection Data Format

JSON fields: latitude, longitude, confidence, severity. PostgreSQL generates the ID.


API Endpoints

POST /detections — saves a detection.GET /detections — retrieves detections.


Docker

Docker Compose will run the components together, with persistent PostgreSQL storage.


Development Goal

Connect all four components using sample data before adding more functionality.
