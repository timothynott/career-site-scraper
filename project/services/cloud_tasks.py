import logging
import os
from typing import Any
from google.cloud import tasks_v2
from scrapy.utils.serialize import ScrapyJSONEncoder


class CloudTasksService:
    def __init__(self):
        self.location = 'us-central1'
        self.project_id = os.environ.get("PROJECT_ID")
        self.google_jwt_service_account = os.environ.get(
            "GOOGLE_JWT_SERVICE_ACCOUNT")
        self.job_board_ingest_api_url = os.environ.get(
            "JOB_BOARD_INGEST_API_URL")

        self.client = tasks_v2.CloudTasksClient()
        # TODO: decouple this service from scrapy. take encoder as optional constructor arg?
        self.encoder = ScrapyJSONEncoder()

    def queue_task(self, queue_name: str, jbi_route: str, payload: Any, http_method: str = 'POST'):
        queue = self.client.queue_path(
            self.project_id, self.location, queue_name)
        url = self.generate_job_board_ingest_url(jbi_route)
        converted_payload = self.encoder.encode(payload).encode('utf-8')
        task = {
            "http_request": {
                "http_method": http_method,
                "url": url,
                "headers": {
                    "Content-Type": "application/json",
                },
                "oidc_token": {
                    "service_account_email": self.google_jwt_service_account,
                    "audience": self.job_board_ingest_api_url,
                },
                "body": converted_payload,
            },
            "schedule_time": {
                "seconds": 0,
            },
        }
        task_request = {
            "parent": queue,
            "task": task,
        }

        response = self.client.create_task(task_request)
        return response

    def generate_job_board_ingest_url(self, jbi_route: str):
        base_url = self.job_board_ingest_api_url.rstrip('/')
        url_path = jbi_route.lstrip('/')
        return '{}/{}'.format(base_url, url_path)
