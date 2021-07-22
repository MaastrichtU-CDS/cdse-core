import json

import responses
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY

TEST_INPUT_PAYLOAD = {
    "Clinical_T": "cT1",
    "Clinical_N": "cN0",
}
TEST_RESULT_PAYLOAD = {"testx": 1, "has_result_page": True}


class TestPredictionApi(TestCase):
    client = None

    def setUp(self) -> None:
        self.client = Client()

    @responses.activate
    def test_ready_api(self):
        client_response = self.client.get(reverse("get_ready"))

        self.assertEqual(client_response.status_code, HTTP_200_OK)
        self.assertEqual(client_response.json(), TEST_INPUT_PAYLOAD)

    @responses.activate
    def test_result_api(self):
        response = self.client.post(
            reverse("post_result"),
            data=json.dumps(TEST_RESULT_PAYLOAD),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTP_200_OK)

    @responses.activate
    def test_incomplete_result_api(self):
        response = self.client.post(
            reverse("post_result"),
            data=json.dumps({"x": 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
