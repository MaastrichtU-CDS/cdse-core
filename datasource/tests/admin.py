from django.contrib.auth.models import User
from django.template.response import TemplateResponse
from django.test import TestCase, Client
from datasource.models import FhirEndpoint


class TestFhirEndpointAdmin(TestCase):
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

    def test_add_fhir_endpoint_trough_form(self):
        self.create_fhir_endpoint(self.name, self.description, self.full_url)

        fhir_obj = FhirEndpoint.objects.filter(pk=1).exists()
        self.assertTrue(fhir_obj)

    def test_title_unique(self):
        self.create_fhir_endpoint(self.name, self.description, self.full_url)
        resp = self.create_fhir_endpoint(self.name, self.description, self.full_url)

        fhir_obj = FhirEndpoint.objects.all()

        self.assertContains(resp, "Fhir endpoint with this Name already exists.")
        self.assertEqual(len(fhir_obj), 1)
