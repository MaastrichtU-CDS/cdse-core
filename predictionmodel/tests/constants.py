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
