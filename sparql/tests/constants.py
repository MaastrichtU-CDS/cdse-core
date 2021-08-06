MODEL_INPUT_SPARQL_QUERY = [
    {
        "fhir_code_child": {"type": "literal", "value": "C48720"},
        "fhir_code_system_child": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "fhir_code_system_parent": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "parent_parameter": {"type": "literal", "value": "Clinical_T"},
        "fhir_code_parent": {"type": "literal", "value": "C48885"},
        "child_parameter": {"type": "literal", "value": "cT1"},
    },
    {
        "fhir_code_child": {"type": "literal", "value": "C48724"},
        "fhir_code_system_child": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "fhir_code_system_parent": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "parent_parameter": {"type": "literal", "value": "Clinical_T"},
        "fhir_code_parent": {"type": "literal", "value": "C48885"},
        "child_parameter": {"type": "literal", "value": "cT2"},
    },
    {
        "fhir_code_child": {"type": "literal", "value": "C48728"},
        "fhir_code_system_child": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "fhir_code_system_parent": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "parent_parameter": {"type": "literal", "value": "Clinical_T"},
        "fhir_code_parent": {"type": "literal", "value": "C48885"},
        "child_parameter": {"type": "literal", "value": "cT3"},
    },
    {
        "fhir_code_child": {"type": "literal", "value": "C48732"},
        "fhir_code_system_child": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "fhir_code_system_parent": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "parent_parameter": {"type": "literal", "value": "Clinical_T"},
        "fhir_code_parent": {"type": "literal", "value": "C48885"},
        "child_parameter": {"type": "literal", "value": "cT4"},
    },
    {
        "fhir_code_child": {"type": "literal", "value": "C48705"},
        "fhir_code_system_child": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "fhir_code_system_parent": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "parent_parameter": {"type": "literal", "value": "Clinical_N"},
        "fhir_code_parent": {"type": "literal", "value": "C48884"},
        "child_parameter": {"type": "literal", "value": "cN0"},
    },
    {
        "fhir_code_child": {"type": "literal", "value": "C48706"},
        "fhir_code_system_child": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "fhir_code_system_parent": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "parent_parameter": {"type": "literal", "value": "Clinical_N"},
        "fhir_code_parent": {"type": "literal", "value": "C48884"},
        "child_parameter": {"type": "literal", "value": "cN1"},
    },
    {
        "fhir_code_child": {"type": "literal", "value": "C48786"},
        "fhir_code_system_child": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "fhir_code_system_parent": {
            "type": "literal",
            "value": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        },
        "parent_parameter": {"type": "literal", "value": "Clinical_N"},
        "fhir_code_parent": {"type": "literal", "value": "C48884"},
        "child_parameter": {"type": "literal", "value": "cN2"},
    },
]

MODEL_INPUT_QUERY_RESULT = [
    {
        "fhir_code_parent": "C48885",
        "fhir_code_system_parent": "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl",
        "parent_parameter": "Clinical_T",
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
