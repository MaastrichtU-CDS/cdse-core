from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase, Client, tag

from django.urls import reverse

from predictionmodel import constants


class TestPredictionModelStartView(TestCase):
    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")

    def tearDown(self):
        self.client.logout()

    @tag("current")
    @patch(
        "predictionmodel.models.query_form_string",
        autospec=True,
        side_effec=Exception(),
    )
    def test_get_model_list_no_response(self, mocked_query):
        mocked_query.return_value = Exception()
        resp = self.client.get(reverse("prediction_start"))
        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "prediction/start.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), constants.ERROR_GET_MODEL_LIST_FAILED)

    @patch(
        "predictionmodel.models.query_form_string",
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

    @patch(
        "predictionmodel.models.query_form_string",
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
    def test_post_with_no_selection(self, mocked_query):
        resp = self.client.post(
            reverse("prediction_start"),
            data={"selected_model_uri": "", "action": "start_prediction"},
            follow=True,
        )

        messages = list(resp.context["messages"])

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), constants.NO_PREDICTION_MODEL_SELECTED)
