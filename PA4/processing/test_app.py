import unittest
from app import generate_mock_data

class TestProcessingComponent(unittest.TestCase):
    def test_mock_data_structure(self):
        """Test the mock data that contains the correct keys and data types."""
        # Call the function
        data = generate_mock_data()

        # Verify the dictionary has the exact same keys the backend expects
        self.assertIn("latitude", data)
        self.assertIn("longitude", data)
        self.assertIn("confidence", data)
        self.assertIn("timestamp", data)

        #Verify the data types are correct for the database
        self.assertIsInstance(data["latitude"], float)
        self.assertIsInstance(data["longitude"], float)
        self.assertIsInstance(data["confidence"], float)
        self.assertIsInstance(data["timestamp"], str)

if __name__ == "__main__":
    unittest.main()