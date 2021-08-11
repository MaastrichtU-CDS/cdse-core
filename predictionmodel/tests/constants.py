from sparql.models import ModelData

FOUND_MODEL_LIST = [
    {
        "model": {
            "type": "uri",
            "value": "https://gitlab.com/leroy.linssen.maastro/test/-/raw/main/rectalcancer.ttl",
        },
        "label": {"type": "literal", "value": "Rectal cancer BN model."},
    }
]

TEST_INPUT_PAYLOAD = {"one": "two"}

TEST_RESULT_PAYLOAD = {"testx": 1, "has_result_page": True}

TEST_MODEL_INPUT_CHILD_PARAMETER = ModelData(
    "C48720",
    "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
    "cT1",
    "T1 Stage Finding",
    None,
    None,
)

TEST_MODEL_INPUT_PARAMETERS = ModelData(
    "C48885",
    "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
    "Clinical_T",
    "Generic Primary Tumor TNM Finding",
    [TEST_MODEL_INPUT_CHILD_PARAMETER],
    None,
)


TEST_PATIENT = {"name": "James Doe", "birthdate": "01-01-1990"}

TEST_OBSERVATIONS = {
    "code": {
        "coding": [
            {
                "code": "C48885",
                "system": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
            }
        ]
    },
    "valueCodeableConcept": {
        "coding": [
            {
                "code": "C48720",
                "system": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
            }
        ]
    },
    "status": "final",
}
