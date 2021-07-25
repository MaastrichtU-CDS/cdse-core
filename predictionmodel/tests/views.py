import json

import responses
from django.contrib.auth.models import User
from django.test import TestCase, Client, tag

from django.urls import reverse

from predictionmodel import constants


class TestPredictionModelStartView(TestCase):
    list_data = [{"name": "BN rectal cancer", "id": 123}]

    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")

    def tearDown(self):
        self.client.logout()

    @responses.activate
    def test_get_model_list_no_response(self):
        responses.add(
            responses.GET,
            "http://localhost:3000/",
            status=500,
        )

        resp = self.client.get(reverse("prediction_start"))
        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prediction/start.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), constants.ERROR_GET_MODEL_LIST_FAILED)

    @responses.activate
    def test_get_model_list_with_item(self):
        responses.add(
            responses.GET,
            "http://localhost:3000/",
            status=200,
            body=json.dumps(self.list_data),
        )

        resp = self.client.get(reverse("prediction_start"))

        self.assertContains(
            resp, '<option value="123">BN rectal cancer</option>', status_code=200
        )
        self.assertTemplateUsed(resp, "prediction/start.html")

    @responses.activate
    def test_post_with_no_selection(self):
        responses.add(
            responses.GET,
            "http://localhost:3000/",
            status=200,
            body=json.dumps(self.list_data),
        )

        resp = self.client.post(
            reverse("prediction_start"),
            data={"select_model_uri": "", "action": "start_prediction"},
            follow=True,
        )

        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), constants.NO_PREDICTION_MODEL_SELECTED)
