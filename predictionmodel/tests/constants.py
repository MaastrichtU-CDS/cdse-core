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
        "fhir_code_parent": "C48885",
        "fhir_code_system_parent": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        "parent_parameter": "Clinical_T",
        "description_parent": "Generic Primary Tumor TNM Finding",
        "child_values": [
            {
                "fhir_code_child": "C48720",
                "fhir_code_system_child": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                "child_parameter": "cT1",
            },
            {
                "fhir_code_child": "C48724",
                "fhir_code_system_child": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                "child_parameter": "cT2",
            },
            {
                "fhir_code_child": "C48728",
                "fhir_code_system_child": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                "child_parameter": "cT3",
            },
            {
                "fhir_code_child": "C48732",
                "fhir_code_system_child": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                "child_parameter": "cT4",
            },
        ],
    },
    {
        "fhir_code_parent": "C48884",
        "fhir_code_system_parent": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        "parent_parameter": "Clinical_N",
        "child_values": [
            {
                "fhir_code_child": "C48705",
                "fhir_code_system_child": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                "child_parameter": "cN0",
            },
            {
                "fhir_code_child": "C48706",
                "fhir_code_system_child": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                "child_parameter": "cN1",
            },
            {
                "fhir_code_child": "C48786",
                "fhir_code_system_child": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
                "child_parameter": "cN2",
            },
        ],
    },
]

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
                "code": "C48728",
                "system": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
            }
        ]
    },
    "status": "final",
}
