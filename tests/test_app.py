import sys
import os
import unittest

sys.path.insert(0, os.path.abspath("app"))

from app import app


class TaskManagerTest(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
