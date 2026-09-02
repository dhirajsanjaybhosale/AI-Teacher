import unittest
from fastapi.testclient import TestClient
from main import app
from app.session_store import student_profile_store

client = TestClient(app)


class TestStudentProfileAndDashboard(unittest.TestCase):

    def test_01_get_student_profile(self):
        res = client.get("/api/profile")
        self.assertEqual(res.status_code, 200)
        data = res.json()

        # Verify Student Personal Information
        self.assertIn("personal_info", data)
        self.assertEqual(data["personal_info"]["full_name"], "Dhiraj Bhosale")
        self.assertEqual(data["personal_info"]["course"], "B.Tech")
        self.assertIn("MMCOE", data["personal_info"]["institution"])

        # Verify Learning Profile
        self.assertIn("learning_profile", data)
        self.assertIn("Exam Preparation", data["learning_profile"]["learning_goals"])

        # Verify Subject & Topic Mastery
        self.assertIn("subjects_mastery", data)
        self.assertTrue(len(data["subjects_mastery"]) >= 3)

        # Verify Misconception Profile
        self.assertIn("misconceptions", data)
        self.assertTrue(len(data["misconceptions"]) >= 1)

        # Verify Learning History
        self.assertIn("learning_history", data)
        self.assertTrue(len(data["learning_history"]) >= 1)

        # Verify Study Plan
        self.assertIn("study_plan", data)
        self.assertTrue(len(data["study_plan"]) >= 5)

    def test_02_update_student_profile(self):
        update_payload = {
            "personal_info": {
                "full_name": "Dhiraj Bhosale",
                "institution": "MMCOE Pune"
            },
            "learning_profile": {
                "preferred_language": "hinglish",
                "daily_study_time_minutes": 75
            }
        }
        res = client.post("/api/profile", json=update_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["personal_info"]["institution"], "MMCOE Pune")
        self.assertEqual(data["learning_profile"]["daily_study_time_minutes"], 75)

    def test_03_record_lesson_completion(self):
        initial_profile = student_profile_store.get_profile()
        initial_lessons = initial_profile.lessons_completed

        record_payload = {
            "topic": "Depth-First Search (DFS)",
            "duration_minutes": 25,
            "quiz_score_percentage": 92,
            "language": "Hinglish"
        }
        res = client.post("/api/profile/record-lesson", json=record_payload)
        self.assertEqual(res.status_code, 200)

        updated_profile = student_profile_store.get_profile()
        self.assertEqual(updated_profile.lessons_completed, initial_lessons + 1)
        self.assertEqual(updated_profile.learning_history[0].topic, "Depth-First Search (DFS)")
        self.assertEqual(updated_profile.learning_history[0].quiz_score_percentage, 92)

    def test_04_update_study_plan(self):
        new_plan = [
            {"day_name": "Monday", "topic": "Graph Representation", "duration_minutes": 30, "is_completed": True},
            {"day_name": "Tuesday", "topic": "BFS", "duration_minutes": 40, "is_completed": False}
        ]
        res = client.post("/api/profile/study-plan", json={"study_plan": new_plan})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["study_plan"]), 2)
        self.assertEqual(data["study_plan"][0]["topic"], "Graph Representation")


if __name__ == "__main__":
    unittest.main()
