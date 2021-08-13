from unittest.mock import patch

from django.test import TestCase

from sparql.query import get_model_input_data
from sparql.tests import MODEL_INPUT_SPARQL_QUERY


class TestInputQuery(TestCase):
    @patch("sparql.query.query_from_string")
    def test_get_model_input_data(self, query_from_string_mock):
        query_from_string_mock.return_value = MODEL_INPUT_SPARQL_QUERY
        result = get_model_input_data("test")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].fhir_code, "C48885")
        self.assertEqual(
            result[0].fhir_code_system,
            "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        )
        self.assertEqual(result[0].parameter, "Clinical_T")
        self.assertEqual(result[0].description, "Generic Primary Tumor TNM Finding")
        self.assertEqual(len(result[0].children), 4)
        self.assertEqual(result[0].children[0].fhir_code, "C48720")
        self.assertEqual(
            result[0].children[0].fhir_code_system,
            "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        )
        self.assertEqual(result[0].children[0].parameter, "cT1")
        self.assertEqual(result[0].children[0].description, "T1 Stage Finding")
