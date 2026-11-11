# RoadWatch Database

This folder contains the PostgreSQL database schema and automated tests for the RoadWatch prototype.

## Files
- `schema.sql` — Creates the detections table used to store pothole coordinates, confidence, and timestamps.
- `database.py` — Contains a function for inserting detection data using SQL.
- `test_database.py` — Contains a unit test using a mock database cursor and an integration test using PostgreSQL.

## Running Tests
With the PostgreSQL Docker container running, execute the following command from the PA4 folder:

`python database/test_database.py`

Both tests should pass when the database is configured correctly.
