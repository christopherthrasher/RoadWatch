import requests # To send HTTP requests to the backend
import time # To pause the script if the backend isn't ready
import json # To format our dictionary nicely
from datetime import datetime # To automatically generate the current time

# The URL where we are sending the data.
# 'backend' must match the service name in compose.yaml
# '8000' must match the port that Vic will set up for his FastAPI server
# '/detections' is the specific route that Vic is building to receive POST requests
API_URL = "http://backend:8000/detections"

# Wrap the data generation in a function to test it.

# Fake pothole record matching the PostgreSQL database schema
def generate_mock_data():
    return {
        "latitude": 39.5296,
        "longitude": -119.8138,
        "confidence": 0.92,
        # Grabs the exact current timeand formats it for the database
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    fake_detection = generate_mock_data()

    # Introductory messages to the Docker terminal logs
    print("Processing contatiner started.")
    print(f"Generated dummy data: {json.dumps(fake_detection)}")
    print("Waiting for the backend to come online....")

    # An infinite loop that keeps trying to send the data until it succeeds
    # preventing the container from crashing if it boots faster than the backend.
    while True:
        try:
            # Attempt to send the fake_detection dictionary as a JSON payload via POST request
            response = requests.post(API_URL, json=fake_detection)

            # HTTP Status 200 (OK) or 201 (Created) means the backend successfully accepted and saved the data
            if response.status_code in [200, 201]:
                print("Success! Backend received the detection.")
                print("Backend Response:", response.json())
                break # Exit the infinite loop since job is done

            # If the backend is running but rejects the data (e.g., wrong format)
            else:
                print(f"Backend is up but returned an error: {response.status_code}. Retrying in 10 seconds...")
                time.sleep(10) # Pause the script for 10 seconds before looping through again

        # This specific connection error triggers if the backend container hasn't fully started yet
        except requests.exceptions.ConnectionError:
            print("Backend not reachable yet. Retrying in 10 seconds...")
            time.sleep(10)
