import os
from urllib.parse import urlencode

from locust import HttpUser, between
import dotenv

dotenv.load_dotenv()


class APIUser(HttpUser):
    wait_time = between(1, 3)
    token = None

    def on_start(self):
        self.login()

    def login(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "username": os.getenv("TEST_USERNAME"),
            "password": os.getenv("TEST_PASSWORD"),
        }

        response = self.client.post(
            "/api/v1/token",
            headers=headers,
            data=urlencode(data)
        )

        if response.status_code == 200:
            self.token = response.json().get("result").get("access_token")
            print(f"Login successful, token: {self.token}")
        else:
            print(f"Login failed: {response.status_code}, {response.text}")
