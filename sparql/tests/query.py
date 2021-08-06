from unittest.mock import patch

from django.test import TestCase

from sparql.query import get_model_input_data
from sparql.tests import MODEL_INPUT_SPARQL_QUERY, MODEL_INPUT_QUERY_RESULT


class TestInputQuery(TestCase):
    @patch("sparql.query.query_from_string")
    def test_get_model_input_data(self, query_from_string_mock):
        query_from_string_mock.return_value = MODEL_INPUT_SPARQL_QUERY
        actual_result = get_model_input_data("test")
        expected_result = MODEL_INPUT_QUERY_RESULT
        self.assertEqual(actual_result, expected_result)
