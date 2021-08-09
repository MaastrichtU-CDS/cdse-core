from sparql.queryExecutor import query_from_string
from sparql.querys.all_models import query_all_models
from sparql.querys.execution_data import query_model_execution_data
from sparql.querys.input_data import query_model_input_data


def get_all_models():
    query_string = query_all_models()
    all_model_data = query_from_string(query_string)
    result = []
    for model in all_model_data:
        new_item = {
            "label": model.get("label").get("value"),
            "uri": model.get("model").get("value"),
        }
        result.append(new_item)
    return result


def get_model_execution_data(selected_model_uri):
    query_string = query_model_execution_data(selected_model_uri)
    execution_data = query_from_string(query_string)

    docker_execution_data = [
        item
        for item in execution_data
        if "docker_execution" in str(item["exec_type"]["value"])
    ]
    return docker_execution_data[0]


def get_model_input_data(selected_model_uri):
    query_string = query_model_input_data(selected_model_uri)
    input_data = query_from_string(query_string)

    unique_parent_inputs = get_unique_parent_list(input_data)
    return add_child_input_to_parent(input_data, unique_parent_inputs)


def get_unique_parent_list(input_data):
    parent_list = []
    for item in input_data:
        parent_list.append(
            {
                "fhir_code_parent": item.get("fhir_code_parent").get("value"),
                "fhir_code_system_parent": item.get("fhir_code_system_parent").get(
                    "value"
                ),
                "parent_parameter": item.get("parent_parameter").get("value"),
                "description_parent": item.get("description_parent").get("value", None),
            }
        )
    return list({item["fhir_code_parent"]: item for item in parent_list}.values())


def add_child_input_to_parent(input_data, parent_input):
    for parent in parent_input:
        parent["child_values"] = []
        for item in input_data:
            if item.get("fhir_code_parent").get("value") in parent["fhir_code_parent"]:
                parent["child_values"].append(
                    {
                        "fhir_code_child": item.get("fhir_code_child").get("value"),
                        "fhir_code_system_child": item.get(
                            "fhir_code_system_child"
                        ).get("value"),
                        "child_parameter": item.get("child_parameter").get("value"),
                        "description_child": item.get("description_child").get(
                            "value", None
                        ),
                    }
                )
    return parent_input


def get_child_parameter_by_code(model_input, child_code):
    for child_input in model_input.get("child_values", []):
        if child_input.get("fhir_code_child") == child_code:
            return child_input
