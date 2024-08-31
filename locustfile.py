import json
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
        with self.client.post(
                "/api/v1/token",
                headers=headers,
                data=urlencode(data),
                catch_response=True
        ) as response:
            if response.status_code == 200:
                try:
                    response_data = json.loads(response.text)
                    if response_data["isSuccess"]:
                        print("응답 성공")
                        self.token = response.json().get("result").get("access_token")
                        response.success()
                    else:
                        print(response_data)
                        response.failure("API 응답 실패")
                except json.JSONDecodeError as e:
                    print(response)
                    response.failure("응답 파싱 실패")
            else:
                response.failure(f"HTTP 상태 코드: {response.status_code}")

    def get_headers(self):
        return {
            "accept": "application/json",
            "access-token": self.token,
            "Content-Type": "application/json"
        }

    def create_quotation(self):
        if not self.token:
            return
        headers = self.get_headers()
        data = {
            "client_id": random.randint(1, 100),
            "created_at": str(date.today()),
            "status": "CREATED"
        }

        with self.client.post("/api/v1/quotations", headers=headers, json=data, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    response_data = json.loads(response.text)
                    if response_data["isSuccess"]:
                        print("응답 성공")
                        response.success()
                    else:
                        print(response_data)
                        response.failure("API 응답 실패")
                except json.JSONDecodeError as e:
                    print(response)
                    response.failure("응답 파싱 실패")
            else:
                response.failure(f"HTTP 상태 코드: {response.status_code}")

    @task(3)
    def add_products_to_quotation(self):
        headers = self.get_headers()

        number_items = random.randint(1, 10)
        items = [{
            "quotation_id": random.randint(1, 100),
            "product_id": random.randint(1, 1000),
            "quantity": random.randint(1, 10)
        }
            for _ in range(number_items)]

        with self.client.post(f"/api/v1/quotations/products", headers=headers, json=items, catch_response=True) as response:
            if response.status_code == 200:
                print("응답 성공")
                try:
                    response_data = json.loads(response.text)
                    if response_data["isSuccess"]:
                        response.success()
                    else:
                        print(response_data)
                        response.failure("API 응답 실패")
                except json.JSONDecodeError as e:
                    print(response)
                    response.failure("응답 파싱 실패")
            else:
                response.failure(f"HTTP 상태 코드: {response.status_code}")