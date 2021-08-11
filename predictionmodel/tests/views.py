import uuid
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, Client

from django.urls import reverse
from fhirclient.models.observation import Observation

from datasource.models import FhirEndpoint
from dockerfacade.exceptions import DockerEngineFailedException
from predictionmodel import constants
from predictionmodel.views import match_input_with_observations, save_prediction_input
from sparql.exceptions import SparqlQueryFailedException
from .constants import (
    FOUND_MODEL_LIST,
    TEST_MODEL_INPUT_PARAMETERS,
    TEST_OBSERVATIONS,
    TEST_PATIENT,
    TEST_MODEL_INPUT_CHILD_PARAMETER,
)
from ..models import PredictionModelSession, PredictionModelData


class TestPredictionModelStartView(TestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")

    def tearDown(self):
        self.client.logout()

    @patch(
        "sparql.query.query_from_string",
        autospec=True,
        side_effect=SparqlQueryFailedException(),
    )
    def test_get_model_list_no_response(self, mocked_query):
        resp = self.client.get(reverse("prediction_start"))
        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prediction/start.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), constants.ERROR_GET_MODEL_LIST_FAILED)

    @patch("sparql.query.query_from_string", return_value=FOUND_MODEL_LIST)
    def test_get_model_list_with_item(self, mocked_query):
        resp = self.client.get(reverse("prediction_start"))

        self.assertContains(resp, "Rectal cancer BN model.", status_code=200)
        self.assertTemplateUsed(resp, "prediction/start.html")


class TestPredictionModelPrepareView(TestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")

    def tearDown(self):
        self.client.logout()

    @patch(
        "predictionmodel.views.get_model_input_data",
        return_value=[TEST_MODEL_INPUT_PARAMETERS],
    )
    @patch("fhir.client.client.FHIRClient")
    @patch(
        "predictionmodel.views.FhirClient.get_patient_name_and_birthdate",
        return_value=TEST_PATIENT,
    )
    @patch(
        "predictionmodel.views.FhirClient.get_patient_observations",
        return_value=[Observation(TEST_OBSERVATIONS)],
    )
    def test_get_view_with_valid_input(
        self,
        get_model_input_data_mock,
        fhir_client_mock,
        get_patient_name_and_birthdate_mock,
        get_patient_observations_mock,
    ):

        FhirEndpoint.objects.create(
            id=1, name="fhir_one", full_url="test-url", is_default=True
        )

        resp = self.client.get(
            reverse("prediction_prepare"),
            data={
                "selected_model_uri": "test",
                "patient_id": "1",
                "fhir_endpoint_id": "1",
            },
            follow=False,
        )

        self.assertTemplateUsed(resp, "prediction/prepare.html")
        self.assertContains(resp, "Name: James Doe", status_code=200)
        self.assertContains(resp, "Birthdate: 01-01-1990", status_code=200)

        self.assertContains(
            resp, "<td>Generic Primary Tumor TNM Finding</td>", status_code=200
        )
        self.assertContains(
            resp,
            """<option value="C48720">T1 Stage Finding</option>""",
            status_code=200,
        )

    def test_post_with_no_model_selection(self):
        resp = self.client.post(
            reverse("prediction_prepare"),
            data={"selected_model_uri": "", "action": "start_prediction"},
            follow=True,
        )

        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), constants.NO_PREDICTION_MODEL_SELECTED)

    @patch(
        "predictionmodel.views.run_model_container",
        side_effect=DockerEngineFailedException(),
    )
    @patch("predictionmodel.views.get_model_execution_data")
    @patch("predictionmodel.views.save_prediction_input")
    def test_post_with_docker_error(
        self,
        run_model_container_mock,
        get_model_execution_data_mock,
        save_prediction_input_mock,
    ):
        resp = self.client.post(
            reverse("prediction_prepare"),
            data={
                "selected_model_uri": "test",
                "action": "start_prediction",
                "patient_id": "1",
                "fhir_endpoint_id": "1",
            },
            follow=True,
        )

        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), constants.ERROR_PREDICTION_MODEL_FAILED)

    @patch("predictionmodel.views.run_model_container")
    @patch(
        "predictionmodel.views.get_model_execution_data",
        side_effect=SparqlQueryFailedException(),
    )
    def test_post_with_model_execution_data_error(
        self, run_model_container_mock, get_model_execution_data_mock
    ):
        resp = self.client.post(
            reverse("prediction_prepare"),
            data={
                "selected_model_uri": "test",
                "action": "start_prediction",
                "patient_id": "1",
                "fhir_endpoint_id": "1",
            },
            follow=True,
        )

        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), constants.ERROR_GET_MODEL_DESCRIPTION_DETAILS_FAILED
        )


class TestHelperFunctions(TestCase):
    def test_matching_observation_and_input(self):
        input_params = [TEST_MODEL_INPUT_PARAMETERS]

        observations_list = [Observation(TEST_OBSERVATIONS)]

        result = match_input_with_observations(input_params, observations_list)

        self.assertEqual(
            result[0].matched_child.fhir_code,
            TEST_MODEL_INPUT_CHILD_PARAMETER.fhir_code,
        )
        self.assertEqual(
            result[0].matched_child.parameter,
            TEST_MODEL_INPUT_CHILD_PARAMETER.parameter,
        )

    @patch(
        "predictionmodel.views.get_model_input_data",
        return_value=[TEST_MODEL_INPUT_PARAMETERS],
    )
    def test_save_prediction_input(self, get_model_input_data_mock):
        post_data = {
            "selected_model_uri": "http://test",
            TEST_MODEL_INPUT_PARAMETERS.fhir_code: TEST_MODEL_INPUT_CHILD_PARAMETER.fhir_code,
        }

        prediction_session = PredictionModelSession.objects.create(
            secret_token=uuid.uuid4(), network_port=1001, user=None
        )
        save_prediction_input(post_data, prediction_session)

        parent_input = PredictionModelData.objects.filter(
            code=TEST_MODEL_INPUT_PARAMETERS.fhir_code
        ).first()
        child_input = PredictionModelData.objects.filter(
            code=TEST_MODEL_INPUT_CHILD_PARAMETER.fhir_code
        ).first()

        self.assertEqual(parent_input.code, TEST_MODEL_INPUT_PARAMETERS.fhir_code)
        self.assertEqual(
            parent_input.input_parameter, TEST_MODEL_INPUT_PARAMETERS.parameter
        )
        self.assertEqual(
            parent_input.system, TEST_MODEL_INPUT_PARAMETERS.fhir_code_system
        )
        self.assertEqual(
            parent_input.system, TEST_MODEL_INPUT_PARAMETERS.fhir_code_system
        )
        self.assertEqual(parent_input.session, prediction_session)
        self.assertEqual(parent_input.session, prediction_session)
        self.assertEqual(parent_input.child_parameter, child_input)

        self.assertEqual(child_input.code, TEST_MODEL_INPUT_CHILD_PARAMETER.fhir_code)
        self.assertEqual(
            child_input.input_parameter, TEST_MODEL_INPUT_CHILD_PARAMETER.parameter
        )
        self.assertEqual(
            child_input.system, TEST_MODEL_INPUT_CHILD_PARAMETER.fhir_code_system
        )
        self.assertEqual(
            child_input.system, TEST_MODEL_INPUT_CHILD_PARAMETER.fhir_code_system
        )
