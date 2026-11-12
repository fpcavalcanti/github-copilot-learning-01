import unittest

from fastapi.testclient import TestClient

from src import app as app_module


class TestParticipantUnregister(unittest.TestCase):
    def setUp(self):
        self.original_activities = app_module.activities
        self.activities = {
            "Chess Club": {
                "participants": [
                    "student@mergington.edu",
                    "other@mergington.edu",
                    "student@mergington.edu",
                ]
            }
        }
        app_module.activities = self.activities
        self.client = TestClient(app_module.app)

    def tearDown(self):
        app_module.activities = self.original_activities
        self.client.close()

    def test_unregister_removes_student_from_activity(self):
        response = self.client.delete(
            "/activities/Chess%20Club/signup",
            params={"email": "student@mergington.edu"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {"message": "Unregistered student@mergington.edu from Chess Club"},
        )
        self.assertEqual(
            self.activities["Chess Club"]["participants"],
            ["other@mergington.edu"],
        )

    def test_unregister_returns_404_for_unknown_activity(self):
        response = self.client.delete(
            "/activities/Unknown%20Club/signup",
            params={"email": "student@mergington.edu"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "Activity not found"})

    def test_unregister_returns_404_for_missing_participant(self):
        response = self.client.delete(
            "/activities/Chess%20Club/signup",
            params={"email": "missing@mergington.edu"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            {"detail": "Student is not signed up for this activity"},
        )


if __name__ == "__main__":
    unittest.main()
