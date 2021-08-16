import uuid
from unittest.mock import patch, MagicMock

from django.contrib.auth.models import User
from django.test import TestCase, Client, TransactionTestCase

from django.urls import reverse
from fhirclient.models.observation import Observation

from datasource.models import FhirEndpoint
from dockerfacade.exceptions import DockerEngineFailedException
from predictionmodel import constants
from predictionmodel.views import (
    match_input_with_observations,
    save_prediction_input,
    create_prediction_session,
)
from sparql.exceptions import SparqlQueryFailedException
from .constants import (
    FOUND_MODEL_LIST,
    TEST_MODEL_INPUT_PARAMETERS,
    TEST_OBSERVATIONS,
    TEST_PATIENT,
    TEST_MODEL_INPUT_CHILD_PARAMETER,
    TEST_SESSION,
    TEST_CONTAINER_PROPS,
    TEST_MODEL_OUTPUT_PARAMETERS,
    TEST_MODEL_OUTPUT_CHILD_PARAMETER,
    TEST_DOCKER_EXECUTION_DATA,
)
from ..constants import ERROR_PREDICTION_CALCULATION, WARNING_SESSION_ENDED
from ..exceptions import CannotSaveModelInputException
from ..models import PredictionModelSession, PredictionModelData, PredictionModelResult


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


class TestPredictionModelPrepareView(TransactionTestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")

        self.endpoint = FhirEndpoint.objects.create(
            name="test_point",
            description="my description",
            full_url="http://test",
            is_default=False,
        )

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

        resp = self.client.get(
            reverse("prediction_prepare"),
            data={
                "selected_model_uri": "test",
                "patient_id": "1",
                "fhir_endpoint_id": self.endpoint.id,
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

    @patch("predictionmodel.views.get_all_models", return_value=[])
    def test_post_with_no_model_selection(self, get_all_models_mock):
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
        "predictionmodel.views.run_container",
        side_effect=DockerEngineFailedException(),
    )
    @patch(
        "predictionmodel.views.create_prediction_session",
        return_value=[MagicMock(), MagicMock()],
    )
    @patch("predictionmodel.views.save_prediction_input")
    @patch("predictionmodel.views.get_all_models", return_value=[])
    def test_post_with_docker_error(
        self,
        run_container_mock,
        create_prediction_session_mock,
        save_prediction_input_mock,
        get_all_models_mock,
    ):
        create_prediction_session_mock.return_value = [
            TEST_SESSION,
            TEST_CONTAINER_PROPS,
        ]
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

    @patch(
        "predictionmodel.views.create_prediction_session",
        side_effect=CannotSaveModelInputException(),
    )
    @patch("predictionmodel.views.save_prediction_input")
    @patch("predictionmodel.views.get_all_models", return_value=[])
    def test_post_with_save_session_error(
        self,
        create_prediction_session_mock,
        save_prediction_input_mock,
        get_all_models_mock,
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
        self.assertEqual(str(messages[0]), constants.ERROR_INPUT_DATA_SAVE_FAILED)

    @patch("predictionmodel.views.run_container")
    @patch(
        "predictionmodel.views.get_model_execution_data",
        side_effect=SparqlQueryFailedException(),
    )
    @patch("predictionmodel.views.get_all_models", return_value=[])
    def test_post_with_model_execution_data_error(
        self,
        run_container_mock,
        get_model_execution_data_mock,
        get_all_models_mock,
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


class TestPredictionModelLoadingView(TransactionTestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")
        self.uuid = uuid.uuid4()
        self.prediction_session = PredictionModelSession.objects.create(
            secret_token=self.uuid, network_port=1001, user=None
        )

    def tearDown(self):
        self.client.logout()

    def test_get_loading_view(self):
        resp = self.client.get(
            reverse("prediction_loading") + "?session_token=" + str(self.uuid)
        )

        self.assertEqual(resp.context["error_message"], ERROR_PREDICTION_CALCULATION)
        self.assertContains(
            resp, """<h1 class="loading-text">Please wait...</h1>""", status_code=200
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prediction/loading.html")

    def test_loading_view_error(self):
        self.prediction_session.error = "A error occurred"

        self.prediction_session.save()
        self.prediction_session.refresh_from_db()

        resp = self.client.get(
            reverse("prediction_loading") + "?session_token=" + str(self.uuid)
        )

        self.assertEqual(resp.context["error_message"], ERROR_PREDICTION_CALCULATION)
        self.assertNotContains(
            resp, """<h1 class="loading-text">Please wait...</h1>""", status_code=200
        )
        self.assertContains(
            resp, """<h1>%s</h1>""" % ERROR_PREDICTION_CALCULATION, status_code=200
        )
        self.assertEqual(resp.status_code, 200)


class TestPredictionModelResultView(TransactionTestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")

        self.uuid = uuid.uuid4()
        self.prediction_session = PredictionModelSession.objects.create(
            secret_token=self.uuid, network_port=1001, user=None
        )

        self.parent_result = PredictionModelResult.objects.create(
            system=TEST_MODEL_OUTPUT_PARAMETERS.fhir_code_system,
            code=TEST_MODEL_OUTPUT_PARAMETERS.fhir_code,
            parameter=TEST_MODEL_OUTPUT_PARAMETERS.parameter,
            parent_parameter=None,
            calculated_value=None,
            session=self.prediction_session,
        )

        self.child_result = PredictionModelResult.objects.create(
            system=TEST_MODEL_OUTPUT_CHILD_PARAMETER.fhir_code_system,
            code=TEST_MODEL_OUTPUT_CHILD_PARAMETER.fhir_code,
            parameter=TEST_MODEL_OUTPUT_CHILD_PARAMETER.parameter,
            parent_parameter=self.parent_result,
            calculated_value="0.1",
            session=None,
        )

    def tearDown(self):
        self.client.logout()

    @patch(
        "predictionmodel.views.get_model_output_data",
        return_value=[TEST_MODEL_OUTPUT_PARAMETERS],
    )
    def test_get_result_view(self, get_model_output_data_mock):
        resp = self.client.get(
            reverse("prediction_result") + "?session_token=" + str(self.uuid)
        )

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, """<td>T0 Stage Finding</td>""", status_code=200)
        self.assertContains(resp, """<td>0.1</td>""", status_code=200)
        self.assertTemplateUsed(resp, "prediction/result.html")

    @patch(
        "predictionmodel.views.get_model_output_data",
        return_value=[TEST_MODEL_OUTPUT_PARAMETERS],
    )
    def test_get_results_without_advanced_view(self, get_model_output_data_mock):
        self.prediction_session.advanced_view = False
        self.prediction_session.save()

        resp = self.client.get(
            reverse("prediction_result") + "?session_token=" + str(self.uuid)
        )

        self.assertNotContains(resp, """iframe""", status_code=200)
        self.assertNotContains(resp, WARNING_SESSION_ENDED, status_code=200)

    @patch(
        "predictionmodel.views.get_model_output_data",
        return_value=[TEST_MODEL_OUTPUT_PARAMETERS],
    )
    def test_get_results_with_advanced_view(self, get_model_output_data_mock):
        self.prediction_session.container_id = "123"
        self.prediction_session.advanced_view = True
        self.prediction_session.save()

        resp = self.client.get(
            reverse("prediction_result") + "?session_token=" + str(self.uuid)
        )

        self.assertContains(
            resp, """<iframe class="not-visible"  id="advanced-view""", status_code=200
        )
        self.assertNotContains(resp, WARNING_SESSION_ENDED, status_code=200)

    @patch(
        "predictionmodel.views.get_model_output_data",
        return_value=[TEST_MODEL_OUTPUT_PARAMETERS],
    )
    def test_get_results_ended_advanced_view(self, get_model_output_data_mock):
        self.prediction_session.container_id = None
        self.prediction_session.advanced_view = True
        self.prediction_session.save()

        resp = self.client.get(
            reverse("prediction_result") + "?session_token=" + str(self.uuid)
        )

        self.assertNotContains(
            resp, """<iframe class="not-visible"  id="advanced-view""", status_code=200
        )
        self.assertContains(resp, WARNING_SESSION_ENDED, status_code=200)

    def test_get_result_view_wrong_token(self):
        resp = self.client.get(reverse("prediction_result"))

        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prediction/result.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), constants.ERROR_PROVIDED_SESSION_TOKEN_INVALID
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
        save_prediction_input(
            post_data, post_data.get("selected_model_uri"), prediction_session
        )

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

    @patch(
        "predictionmodel.views.get_model_execution_data",
        return_value=TEST_DOCKER_EXECUTION_DATA,
    )
    def test_create_prediction_session(self, get_model_execution_data_mock):
        fhir_endpoint = FhirEndpoint.objects.create(
            name="test_point",
            description="my description",
            full_url="http://test",
            is_default=False,
        )

        selected_model_uri = "http://test"
        patient_id = "1"

        prediction_session, container_values = create_prediction_session(
            selected_model_uri, patient_id, fhir_endpoint.id, None
        )

        self.assertEqual(prediction_session.patient_id, patient_id)
        self.assertEqual(prediction_session.data_source, fhir_endpoint)
        self.assertEqual(prediction_session.image_name, "lery/bn-test:latest")
        self.assertEqual(
            prediction_session.image_id,
            "sha256:d1a150476cc5cb6424dacafc8b6ca4195ad41a81bd3d95a853d7ee95767004c8",
        )
        self.assertFalse(prediction_session.calculation_complete)
        self.assertEqual(prediction_session.model_uri, selected_model_uri)

    @patch(
        "predictionmodel.views.get_model_execution_data",
        return_value=TEST_DOCKER_EXECUTION_DATA,
    )
    def test_invalid_prediction_session(self, get_model_execution_data_mock):
        fhir_endpoint = FhirEndpoint.objects.create(
            name="test_point",
            description="my description",
            full_url="http://test",
            is_default=False,
        )

        selected_model_uri = "http://test"

        with self.assertRaises(CannotSaveModelInputException):
            prediction_session, container_values = create_prediction_session(
                selected_model_uri, None, fhir_endpoint.id, None
            )
