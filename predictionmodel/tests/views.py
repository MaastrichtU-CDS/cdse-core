import json

import responses
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY


class TestPredictionModelView(TestCase):
    client = None
    TEST_INPUT_PAYLOAD = {
        "clinical_T": "cT1",
        "clinical_N": "cN0",
    }
    TEST_RESULT_PAYLOAD = {"testx": 1, "has_result_page": True}

    def setUp(self) -> None:
        self.client = Client()

    @responses.activate
    def test_ready_view(self):
        responses.add(
            responses.POST,
            "http://localhost:1312/",
            status=200,
        )

        client_response = self.client.get(reverse("get_ready"))

        self.assertEqual(client_response.status_code, HTTP_200_OK)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.body, json.dumps(self.TEST_INPUT_PAYLOAD)
        )

    @responses.activate
    def test_result_view(self):
        response = self.client.post(
            reverse("post_result"),
            data=json.dumps(self.TEST_RESULT_PAYLOAD),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTP_200_OK)

    @responses.activate
    def test_incomplete_result_view(self):
        response = self.client.post(
            reverse("post_result"),
            data=json.dumps({"x": 1}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, HTTP_422_UNPROCESSABLE_ENTITY)
