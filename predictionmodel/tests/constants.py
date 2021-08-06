FOUND_MODEL_LIST = [
    {
        "model": {
            "type": "uri",
            "value": "https://gitlab.com/leroy.linssen.maastro/test/-/raw/main/rectalcancer.ttl",
        },
        "label": {"type": "literal", "value": "Rectal cancer BN model."},
    }
]

TEST_INPUT_PAYLOAD = {
    "Clinical_T": "cT1",
    "Clinical_N": "cN0",
}

TEST_RESULT_PAYLOAD = {"testx": 1, "has_result_page": True}

TEST_MODEL_INPUT_PARAMETERS = [
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


TEST_OBSERVATIONS = {
    "code": {"coding": [{"code": "C48885", "system": "ncit"}]},
    "valueCodeableConcept": {"coding": [{"code": "C48728", "system": "ncit"}]},
    "status": "final",
}
