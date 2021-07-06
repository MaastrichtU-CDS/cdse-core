from unittest.mock import patch
import responses
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from django.contrib import messages

from datasource import constants
from datasource.admin import FhirEndpointAdmin
from datasource.models import FhirEndpoint


@patch("django.contrib.messages.add_message", autospec=True)
class TestFhirEndpointAdminFunction(TestCase):
    def setUp(self):
        self.fhirEndpointAdmin = FhirEndpointAdmin(
            model=FhirEndpoint, admin_site=AdminSite()
        )
        self.meta_data_json = {
            "fhirVersion": "5.0.1",
            "format": ["application/fhir+xml", "application/fhir+json"],
            "kind": "instance",
            "status": "active",
            "date": "2021-07-04T11:40:25+00:00",
        }

        self.form_obj = FhirEndpoint
        self.form_obj.name = "test"
        self.form_obj.full_url = "http://localhost:8080/fhir"

        self.request = HttpRequest()
        self.request.POST.appendlist("_test", "test")

    def test_endpoint_no_response(self, mock_add_message):
        self.assertRaises(
            Exception,
            self.fhirEndpointAdmin.response_change(self.request, self.form_obj),
        )
        mock_add_message.assert_called_once_with(
            self.request, messages.ERROR, constants.TEST_ERROR_UNKNOWN
        )

    @responses.activate
    def test_endpoint_not_found(self, mock_add_message):
        responses.add(
            responses.GET,
            "http://localhost:8080/fhir/metadata",
            status=404,
        )

        self.assertRaises(
            Exception,
            self.fhirEndpointAdmin.response_change(self.request, self.form_obj),
        )
        mock_add_message.assert_called_once_with(
            self.request,
            messages.ERROR,
            constants.TEST_ERROR_404,
        )

    @responses.activate
    def test_endpoint_not_authorized(self, mock_add_message):
        responses.add(
            responses.GET,
            "http://localhost:8080/fhir/metadata",
            status=401,
        )

        self.assertRaises(
            Exception,
            self.fhirEndpointAdmin.response_change(self.request, self.form_obj),
        )
        mock_add_message.assert_called_once_with(
            self.request,
            messages.ERROR,
            constants.TEST_ERROR_401,
        )

    @responses.activate
    def test_endpoint_no_rights(self, mock_add_message):
        responses.add(
            responses.GET,
            "http://localhost:8080/fhir/metadata",
            status=403,
        )

        self.assertRaises(
            Exception,
            self.fhirEndpointAdmin.response_change(self.request, self.form_obj),
        )
        mock_add_message.assert_called_once_with(
            self.request,
            messages.ERROR,
            constants.TEST_ERROR_403,
        )

    @responses.activate
    def test_endpoint_wrong_version(self, mock_add_message):
        responses.add(
            responses.GET,
            "http://localhost:8080/fhir/metadata",
            json=self.meta_data_json,
            status=200,
        )
        self.assertRaises(
            Exception,
            self.fhirEndpointAdmin.response_change(self.request, self.form_obj),
        )
        mock_add_message.assert_called_once_with(
            self.request,
            messages.WARNING,
            constants.TEST_ERROR_VERSION,
        )

    @responses.activate
    def test_endpoint_right_version(self, mock_add_message):
        self.meta_data_json["fhirVersion"] = "4.0.1"

        responses.add(
            responses.GET,
            "http://localhost:8080/fhir/metadata",
            json=self.meta_data_json,
            status=200,
        )
        self.assertRaises(
            Exception,
            self.fhirEndpointAdmin.response_change(self.request, self.form_obj),
        )
        mock_add_message.assert_called_once_with(
            self.request,
            messages.INFO,
            constants.TEST_SUCCESS,
        )


class TestFhirEndpointAdminApi(TestCase):
    name = "test_endpoint"
    description = "here a test description"
    full_url = "http://127.0.0.1/"

    def setUp(self):
        User.objects.create_superuser("admin", "admin@example.com", "Password123")
        self.client = Client()
        self.client.login(username="admin", password="Password123")

    def tearDown(self):
        self.client.logout()

    def create_fhir_endpoint(self, name, description, full_url) -> TemplateResponse:
        response = self.client.post(
            "/admin/datasource/fhirendpoint/add/",
            {"name": name, "description": description, "full_url": full_url},
            follow=True,
        )

        return response

    def test_add_fhir_endpoint(self):
        self.create_fhir_endpoint(self.name, self.description, self.full_url)

        fhir_obj = FhirEndpoint.objects.filter(pk=1).exists()
        self.assertTrue(fhir_obj)

    def test_title_unique(self):
        self.create_fhir_endpoint(self.name, self.description, self.full_url)
        resp = self.create_fhir_endpoint(self.name, self.description, self.full_url)

        fhir_obj = FhirEndpoint.objects.all()

        self.assertContains(resp, constants.CONSTRAINT_ERROR_UNIQUE_NAME)
        self.assertEqual(len(fhir_obj), 1)
