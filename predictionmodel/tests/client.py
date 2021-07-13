import json
import responses
from django.test import TestCase
from predictionmodel.client import Client


class TestPredictionModelClient(TestCase):
    @responses.activate
    def test_client_input(self):
        responses.add(
            responses.POST,
            "http://localhost:1312/",
            status=200,
        )

        Client().post_model_input()

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.headers.get("Authorization"), "secret"
        )
        self.assertEqual(
            json.loads(responses.calls[0].request.body).get("clinical_T"), "cT1"
        )
        self.assertEqual(
            json.loads(responses.calls[0].request.body).get("clinical_N"), "cN0"
        )

    @responses.activate
    def test_client_result(self):
        responses.add(
            responses.GET,
            "http://localhost:1312/",
            status=200,
        )

        Client().get_model_result_page()

        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(
            responses.calls[0].request.headers.get("Authorization"), "secret"
        )
