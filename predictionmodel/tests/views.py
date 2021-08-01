from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, Client, tag

from django.urls import reverse
from fhirclient.models.observation import Observation

from dockerfacade.exceptions import DockerEngineFailedException
from predictionmodel import constants
from predictionmodel.views import match_input_with_observations
from sparql.exceptions import SparqlQueryFailedException


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

    @patch(
        "sparql.query.query_from_string",
        return_value=[
            {
                "model": {
                    "type": "uri",
                    "value": "https://gitlab.com/leroy.linssen.maastro/test/-/raw/main/rectalcancer.ttl",
                },
                "label": {"type": "literal", "value": "Rectal cancer BN model."},
            }
        ],
    )
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
    def test_post_with_docker_error(
        self, run_model_container_mock, get_model_execution_data_mock
    ):
        resp = self.client.post(
            reverse("prediction_prepare"),
            data={"selected_model_uri": "test", "action": "start_prediction"},
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
            data={"selected_model_uri": "test", "action": "start_prediction"},
            follow=True,
        )

        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), constants.ERROR_GET_MODEL_DESCRIPTION_DETAILS_FAILED
        )

    def test_matching_observation_and_input(self):
        input_params = [
            {
                "code_parent": "C48885",
                "input_type_parent": "ncit",
                "parent_input_parameter": "Clinical_T",
                "child_values": [
                    {
                        "code_child": "C48728",
                        "input_type_child": "ncit",
                        "model_input_parameter": "cT3",
                    },
                    {
                        "code_child": "C48732",
                        "input_type_child": "ncit",
                        "model_input_parameter": "cT4",
                    },
                ],
            },
            {
                "code_parent": "C48884",
                "input_type_parent": "ncit",
                "parent_input_parameter": "Clinical_N",
                "child_values": [
                    {
                        "code_child": "C48705",
                        "input_type_child": "ncit",
                        "model_input_parameter": "cN0",
                    },
                    {
                        "code_child": "C48706",
                        "input_type_child": "ncit",
                        "model_input_parameter": "cN1",
                    },
                ],
            },
        ]

        observations_list = [
            Observation(
                {
                    "code": {"coding": [{"code": "C48885", "system": "ncit"}]},
                    "valueCodeableConcept": {
                        "coding": [{"code": "C48728", "system": "ncit"}]
                    },
                    "status": "final",
                }
            )
        ]

        result = match_input_with_observations(input_params, observations_list)

        self.assertEqual(
            result[0].get("matching_child_input").get("code_child"), "C48728"
        )
        self.assertEqual(result[1].get("matching_child_input"), None)
