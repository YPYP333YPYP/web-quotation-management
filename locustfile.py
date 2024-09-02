import json
import os
import random
from datetime import date
from urllib.parse import urlencode

from locust import HttpUser, between, task, TaskSet
import dotenv

dotenv.load_dotenv()


# 고객이 견적서 생성 후 물품 추가 이후 견적서 정보 조회
class OrderServiceBehavior(TaskSet):
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
                        return response_data["result"]["id"]
                    else:
                        print(response_data)
                        response.failure("API 응답 실패")
                except json.JSONDecodeError as e:
                    print(response)
                    response.failure("응답 파싱 실패")
            else:
                response.failure(f"HTTP 상태 코드: {response.status_code}")

    def add_products_to_quotation(self, quotation_id):
        headers = self.get_headers()

        number_items = random.randint(1, 10)
        items = [{
            "quotation_id": quotation_id,
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

    def view_quotation(self, quotation_id):
        headers = self.get_headers()

        with self.client.get(f"/api/v1/quotations/{quotation_id}", headers=headers, catch_response=True) as response:
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

    @task(1)
    def complex_scenario(self):
        quotation_id = self.create_quotation()
        if quotation_id:
            self.add_products_to_quotation(quotation_id)
            self.view_quotation(quotation_id)


class PastOrderServiceBehavior(TaskSet):
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

    def create_past_order(self):
        if not self.token:
            return
        headers = self.get_headers()

        random_client_id = random.randint(1, 100)
        random_number = random.randint(1, 30)
        product_ids = [x for x in range(random_number)]

        data = {
            "client_id": random_client_id,
            "name": f"past-order-{random_client_id}",
            "product_ids": product_ids
        }

        with self.client.post("/api/v1/past-order", headers=headers, json=data, catch_response=True) as response:
            if response.status_code == 200:
                try:
                    response_data = json.loads(response.text)
                    if response_data["isSuccess"]:
                        print("응답 성공")
                        response.success()
                        return response_data["result"]
                    else:
                        print(response_data)
                        response.failure("API 응답 실패")
                except json.JSONDecodeError as e:
                    print(response)
                    response.failure("응답 파싱 실패")
            else:
                response.failure(f"HTTP 상태 코드: {response.status_code}")

    def add_products_to_past_order(self, past_order_id):
        headers = self.get_headers()

        product_id = random.randint(1, 1000)

        with self.client.post(f"/api/v1/past-order/{past_order_id}/{product_id}/update", headers=headers,
                              catch_response=True) as response:
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

    def view_quotation(self, past_order_id):
        headers = self.get_headers()

        with self.client.get(f"/api/v1/past-order/{past_order_id}", headers=headers, catch_response=True) as response:
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

    @task(1)
    def complex_scenario(self):
        past_order_id = self.create_past_order()
        if past_order_id:
            self.add_products_to_past_order(past_order_id)
            self.view_quotation(past_order_id)


class WebsiteUser(HttpUser):
    tasks = [OrderServiceBehavior, PastOrderServiceBehavior]
    wait_time = between(1, 3)