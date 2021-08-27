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
    TEST_MODEL_OUTPUT_CHILD_PARAMETER,
)
from ..models import PredictionModelSession, PredictionModelData, PredictionModelResult


class TestPredictionApi(TransactionTestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.uuid = uuid.uuid4()
        self.prediction_session = PredictionModelSession.objects.create(
            secret_token=self.uuid, network_port=1001, user=None, container_id="sha256"
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
            session=self.prediction_session,
        )

    @responses.activate
    def test_ready_api(self):
        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}
        client_response = self.client.get(reverse("get_model_input"), **headers)

        self.assertEqual(client_response.status_code, HTTP_200_OK)
        self.assertEqual(client_response.json(), TEST_INPUT_PAYLOAD)

    @responses.activate
    def test_ready_api_stopped_session(self):
        self.prediction_session.container_id = None
        self.prediction_session.save()
        self.prediction_session.refresh_from_db()

        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}
        response = self.client.get(reverse("get_model_input"), **headers)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @responses.activate
    def test_ready_api_wrong_token(self):
        response = self.client.get(reverse("get_model_input"))

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

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

        self.prediction_session.refresh_from_db()
        results = PredictionModelResult.objects.all()

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].code, TEST_MODEL_OUTPUT_PARAMETERS.fhir_code)
        self.assertEqual(
            results[0].system, TEST_MODEL_OUTPUT_PARAMETERS.fhir_code_system
        )
        self.assertEqual(results[0].parameter, TEST_MODEL_OUTPUT_PARAMETERS.parameter)

        self.assertEqual(results[1].code, TEST_MODEL_OUTPUT_CHILD_PARAMETER.fhir_code)
        self.assertEqual(
            results[1].system, TEST_MODEL_OUTPUT_CHILD_PARAMETER.fhir_code_system
        )
        self.assertEqual(
            results[1].parameter, TEST_MODEL_OUTPUT_CHILD_PARAMETER.parameter
        )
        self.assertEqual(
            results[1].parameter, TEST_MODEL_OUTPUT_CHILD_PARAMETER.parameter
        )
        self.assertEqual(
            results[1].calculated_value,
            str(TEST_RESULT_PAYLOAD.get("Pathological_T").get("ypT0")),
        )

        self.assertEqual(self.prediction_session.calculation_complete, True)
        self.assertEqual(response.status_code, HTTP_200_OK)

    @responses.activate
    def test_result_api_stopped_session(self):
        self.prediction_session.container_id = None
        self.prediction_session.save()
        self.prediction_session.refresh_from_db()

        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}
        response = self.client.post(
            reverse("post_result"),
            data=json.dumps(TEST_RESULT_PAYLOAD),
            content_type="application/json",
            **headers
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @responses.activate
    def test_result_api_wrong_token(self):
        headers = {"HTTP_AUTHORIZATION": "secret"}

        response = self.client.post(
            reverse("post_result"),
            data=json.dumps(TEST_RESULT_PAYLOAD),
            content_type="application/json",
            **headers
        )

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @responses.activate
    def test_check_calculation_incomplete(self):
        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}

        response = self.client.get(reverse("check_result"), **headers)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(
            response.json(), {"calculation_complete": False, "error": None}
        )

    @responses.activate
    def test_check_calculation_complete(self):
        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}

        self.prediction_session.calculation_complete = True
        self.prediction_session.save()

        response = self.client.get(reverse("check_result"), **headers)

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.json(), {"calculation_complete": True, "error": None})

    @responses.activate
    def test_check_calculation_stopped_session(self):
        self.prediction_session.container_id = None
        self.prediction_session.save()
        self.prediction_session.refresh_from_db()

        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}
        response = self.client.get(reverse("check_result"), **headers)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @responses.activate
    def test_check_calculation_wrong_token(self):
        headers = {"HTTP_AUTHORIZATION": "secret"}

        response = self.client.get(reverse("check_result"), **headers)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @responses.activate
    def test_calculation_error(self):
        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}
        test_error_message = "There was a error"
        response = self.client.post(
            reverse("calculation_error"),
            data=json.dumps({"error_message": test_error_message}),
            content_type="application/json",
            **headers
        )

        self.prediction_session.refresh_from_db()

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(self.prediction_session.error, test_error_message)

    @responses.activate
    def test_calculation_error_stopped_session(self):
        self.prediction_session.container_id = None
        self.prediction_session.save()
        self.prediction_session.refresh_from_db()

        headers = {"HTTP_AUTHORIZATION": str(self.uuid)}
        response = self.client.post(reverse("calculation_error"), **headers)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)

    @responses.activate
    def test_calculation_error_wrong_token(self):
        headers = {"HTTP_AUTHORIZATION": "secret"}

        response = self.client.post(reverse("calculation_error"), **headers)

        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
