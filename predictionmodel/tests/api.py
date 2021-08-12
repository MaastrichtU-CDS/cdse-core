import json
import uuid
from unittest.mock import patch

import responses
from django.test import TransactionTestCase, Client
from django.urls import reverse
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_403_FORBIDDEN,
)

from .constants import (
    TEST_INPUT_PAYLOAD,
    TEST_RESULT_PAYLOAD,
    TEST_MODEL_OUTPUT_PARAMETERS,
)
from ..models import PredictionModelSession, PredictionModelData


class TestPredictionApi(TransactionTestCase):
    client = None
    uuid = None

    def setUp(self) -> None:
        self.client = Client()
        self.uuid = uuid.uuid4()
        prediction_session = PredictionModelSession.objects.create(
            secret_token=self.uuid, network_port=1001, user=None
        )

        model_input_data_child = PredictionModelData.objects.create(
            system="ncit",
            code="002",
            input_parameter="cT1",
            child_parameter=None,
        )

        PredictionModelData.objects.create(
            system="ncit",
            code="001",
            input_parameter="Clinical_T",
            child_parameter=model_input_data_child,
            session=prediction_session,
        )

    @responses.activate
    def test_ready_api(self):
        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}
        client_response = self.client.get(reverse("get_model_input"), **headers)

        self.assertEqual(client_response.status_code, HTTP_200_OK)
        self.assertEqual(client_response.json(), TEST_INPUT_PAYLOAD)

    @responses.activate
    def test_ready_api_wrong_token(self):
        client_response = self.client.get(reverse("get_model_input"))

        self.assertEqual(client_response.status_code, HTTP_403_FORBIDDEN)

    @responses.activate
    @patch(
        "predictionmodel.api.get_model_output_data",
        return_value=[TEST_MODEL_OUTPUT_PARAMETERS],
    )
    def test_result_api(self, get_model_output_data_mock):
        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}

        response = self.client.post(
            reverse("post_result"),
            data=json.dumps(TEST_RESULT_PAYLOAD),
            content_type="application/json",
            **headers
        )

        self.assertEqual(response.status_code, HTTP_200_OK)
