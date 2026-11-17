
import unittest
from app import app


class SpiceRouteTests(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_valid_inquiry(self):
        response = self.client.post(
            "/api/inquiries",
            json={
                "guest_name": "Ammara",
                "guest_message": "I want to book a table.",
                "party_size": 4
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json["success"])

    def test_missing_guest_message(self):
        response = self.client.post(
            "/api/inquiries",
            json={"guest_name": "Ammara"}
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_party_size(self):
        response = self.client.post(
            "/api/inquiries",
            json={
                "guest_name": "Ammara",
                "guest_message": "Need a table.",
                "party_size": 15
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_menu_endpoint(self):
        response = self.client.get("/api/menu")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
