from django.test import TestCase
from datasource.models import FhirEndpoint
from django.core.exceptions import ValidationError


class TestFhirEndpoint(TestCase):
    def test_create_endpoint(self):
        name = "fhir_obj"
        description = "this is my test"
        full_url = "http://127.0.0.1/fhir"
        is_default = True

        fhir_obj = FhirEndpoint.objects.create(
            name=name, description=description, full_url=full_url, is_default=is_default
        )

        self.assertEqual(fhir_obj.name, name)
        self.assertEqual(fhir_obj.description, description)
        self.assertEqual(fhir_obj.full_url, full_url)
        self.assertEqual(fhir_obj.is_default, is_default)

    def test_single_default_allowed(self):
        fhir_obj_one = FhirEndpoint.objects.create(name="fhir_one", is_default=True)
        fhir_obj_two = FhirEndpoint.objects.create(name="fhir_two", is_default=True)
        self.assertEqual(fhir_obj_one.is_default, True)
        self.assertRaises(ValidationError, fhir_obj_two.clean)
