from locust import HttpUser, task, between


class MockUser(HttpUser):
    wait_time = between(45, 60)

    @task
    def send_request(self):
        data = {"prompt": "cookie"}
        self.client.post("/api/v1/text-to-image/", json=data)
