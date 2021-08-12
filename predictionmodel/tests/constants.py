import uuid

from predictionmodel.models import PredictionModelSession
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

TEST_INPUT_PAYLOAD = {"Clinical_T": "cT1"}

TEST_RESULT_PAYLOAD = {
    "Pathological_T": {
        "ypT0": 0.1,
    },
    "has_result_page": False,
}

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

TEST_MODEL_OUTPUT_CHILD_PARAMETER = ModelData(
    "C48719",
    "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
    "ypT0",
    "T0 Stage Finding",
    None,
    None,
)

TEST_MODEL_OUTPUT_PARAMETERS = ModelData(
    "C48888",
    "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
    "Pathological_T",
    "Pathologic Primary Tumor TNM Finding",
    [TEST_MODEL_OUTPUT_CHILD_PARAMETER],
    None,
)

TEST_SESSION = PredictionModelSession(
    image_name="test", image_id="123", network_port=12, secret_token=uuid.uuid4()
)

TEST_CONTAINER_PROPS = {"invocation_url": "http://test"}

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
