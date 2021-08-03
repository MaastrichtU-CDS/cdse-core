from unittest.mock import patch

from django.test import TestCase, tag

from sparql.query import get_model_input_data


class TestInputQuery(TestCase):
    input_data = [
        {
            "input_type_parent": {"type": "literal", "value": "ncit"},
            "input_type_child": {"type": "literal", "value": "ncit"},
            "code_child": {"type": "literal", "value": "C48720"},
            "parent_input_parameter": {"type": "literal", "value": "Clinical_T"},
            "code_parent": {"type": "literal", "value": "C48885"},
            "model_input_parameter": {"type": "literal", "value": "cT1"},
        },
        {
            "input_type_parent": {"type": "literal", "value": "ncit"},
            "input_type_child": {"type": "literal", "value": "ncit"},
            "code_child": {"type": "literal", "value": "C48724"},
            "parent_input_parameter": {"type": "literal", "value": "Clinical_T"},
            "code_parent": {"type": "literal", "value": "C48885"},
            "model_input_parameter": {"type": "literal", "value": "cT2"},
        },
        {
            "input_type_parent": {"type": "literal", "value": "ncit"},
            "input_type_child": {"type": "literal", "value": "ncit"},
            "code_child": {"type": "literal", "value": "C48728"},
            "parent_input_parameter": {"type": "literal", "value": "Clinical_T"},
            "code_parent": {"type": "literal", "value": "C48885"},
            "model_input_parameter": {"type": "literal", "value": "cT3"},
        },
        {
            "input_type_parent": {"type": "literal", "value": "ncit"},
            "input_type_child": {"type": "literal", "value": "ncit"},
            "code_child": {"type": "literal", "value": "C48732"},
            "parent_input_parameter": {"type": "literal", "value": "Clinical_T"},
            "code_parent": {"type": "literal", "value": "C48885"},
            "model_input_parameter": {"type": "literal", "value": "cT4"},
        },
        {
            "input_type_parent": {"type": "literal", "value": "ncit"},
            "input_type_child": {"type": "literal", "value": "ncit"},
            "code_child": {"type": "literal", "value": "C48705"},
            "parent_input_parameter": {"type": "literal", "value": "Clinical_N"},
            "code_parent": {"type": "literal", "value": "C48884"},
            "model_input_parameter": {"type": "literal", "value": "cN0"},
        },
        {
            "input_type_parent": {"type": "literal", "value": "ncit"},
            "input_type_child": {"type": "literal", "value": "ncit"},
            "code_child": {"type": "literal", "value": "C48706"},
            "parent_input_parameter": {"type": "literal", "value": "Clinical_N"},
            "code_parent": {"type": "literal", "value": "C48884"},
            "model_input_parameter": {"type": "literal", "value": "cN1"},
        },
        {
            "input_type_parent": {"type": "literal", "value": "ncit"},
            "input_type_child": {"type": "literal", "value": "ncit"},
            "code_child": {"type": "literal", "value": "C48786"},
            "parent_input_parameter": {"type": "literal", "value": "Clinical_N"},
            "code_parent": {"type": "literal", "value": "C48884"},
            "model_input_parameter": {"type": "literal", "value": "cN2"},
        },
    ]

    @patch("sparql.query.query_from_string")
    def test_get_model_input_data(self, query_from_string_mock):
        query_from_string_mock.return_value = self.input_data
        actual_result = get_model_input_data("test")
        expected_result = [
            {
                "code_parent": "C48885",
                "input_type_parent": "ncit",
                "parent_input_parameter": "Clinical_T",
                "child_values": [
                    {
                        "code_child": "C48720",
                        "input_type_child": "ncit",
                        "model_input_parameter": "cT1",
                    },
                    {
                        "code_child": "C48724",
                        "input_type_child": "ncit",
                        "model_input_parameter": "cT2",
                    },
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
                    {
                        "code_child": "C48786",
                        "input_type_child": "ncit",
                        "model_input_parameter": "cN2",
                    },
                ],
            },
        ]
        self.assertEqual(actual_result, expected_result)
