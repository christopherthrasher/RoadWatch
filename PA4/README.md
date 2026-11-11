# RoadWatch PA4 Prototype

## Project Overview

RoadWatch is a pothole detection system designed to help identify and track road damage. This prototype demonstrates how sample pothole detection data moves between the processing component, backend, PostgreSQL database, and web interface.

## Components

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS, Node.js
- **Backend:** Python, FastAPI
- **Database:** PostgreSQL
- **Processing:** Python
- **Containerization:** Docker Compose

## Detection Data Format

Each detection contains the following JSON fields:
- `latitude`
- `longitude`
- `confidence`
- `timestamp`

PostgreSQL automatically generates a unique ID for each detection.

## API Endpoints

- `GET /health` — Checks backend availability.
- `POST /detections` — Saves a detection to PostgreSQL.
- `GET /detections` — Retrieves stored detections.

## Running the Prototype

1. Install and open Docker Desktop.
2. Open a terminal in the `PA4` folder.
3. Run:

   `docker compose up -d --build`

4. Access the components:
   - **Frontend:** http://localhost:3000
   - **Backend:** http://localhost:8000
   - **Detection API:** http://localhost:8000/detections

To generate another sample detection, run:

`docker compose restart processing`

## Database

PostgreSQL runs through Docker Compose with persistent storage.

The database table is defined in `database/schema.sql`. Run this SQL file against the `roadwatch` database to create the detections table.

The backend connects to PostgreSQL using the service name `database` and port `5432` inside Docker. Connections from the host computer use `localhost:5433`.

Database credentials for the local prototype are defined in `compose.yaml`.

## Testing

The RoadWatch prototype includes automated tests for the frontend, backend, database, and processing components.

- **Frontend:** Uses Vitest to test that the Container component correctly renders its children and optional class name.
- **Backend:** Uses Python's unittest framework to verify input validation, including rejecting invalid detection coordinates.
- **Database:** Includes a unit test using a mock database cursor to verify the SQL INSERT operation and an integration test that inserts and retrieves detection data from PostgreSQL.
- **Processing:** Tests that generated sample pothole detection data contains the expected fields and data types.

The prototype was also tested by sending sample detections to the backend, storing them in PostgreSQL, and retrieving them through the frontend.

## Current Prototype Limitations

The processing component currently generates sample pothole data rather than detecting potholes from actual video.

The frontend demonstrates basic API communication, but the interactive pothole map and other planned features are not yet implemented.
