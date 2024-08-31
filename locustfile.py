import os
import random
from datetime import date
from urllib.parse import urlencode

from locust import HttpUser, between, task
import dotenv

dotenv.load_dotenv()


# 고객이 견적서 생성 후 물품 추가 이후 견적서 정보 조회
class OrderServiceUser(HttpUser):
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

        if response.code == 200:
            self.token = response.json().get("result").get("access_token")
            print(f"Login successful, token: {self.token}")
        else:
            print(f"Login failed: {response.status_code}, {response.text}")

    def get_headers(self):
        return {
            "accept": "application/json",
            "access-token": self.token,
            "Content-Type": "application/json"
        }

    @task(3)
    def create_quotation(self):
        if not self.token:
            return
        headers = self.get_headers()
        data = {
            "client_id": random.randint(1, 100),
            "created_at": str(date.today()),
            "status": "CREATED"
        }
        response = self.client.post("/api/v1/quotations", headers=headers, json=data)
        if response.code == 200:
            print(f"Quotation created successfully: {response.json()}")
        else:
            print(f"Failed to create quotation: {response.status_code}, {response.text}")

