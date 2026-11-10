
def insert_detection(cursor, latitude, longitude, confidence, timestamp):
    cursor.execute(
        """
        INSERT INTO detections (latitude, longitude, confidence, timestamp)
        VALUES (%s, %s, %s, %s);
        """,
        (latitude, longitude, confidence, timestamp)
    )
