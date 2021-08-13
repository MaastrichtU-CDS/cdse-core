from sparql.models import ModelInput
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

    parent_inputs = get_parent_list(input_data)
    return add_child_input_to_parent(input_data, parent_inputs)


def get_parent_list(input_data):
    parent_list: list(ModelInput) = []

    for item in list(
        {
            item.get("fhir_code_parent").get("value"): item for item in input_data
        }.values()
    ):
        parent_list.append(
            ModelInput(
                item.get("fhir_code_parent").get("value"),
                item.get("fhir_code_system_parent").get("value"),
                item.get("parent_parameter").get("value"),
                item.get("description_parent").get("value", None),
                [],
                None,
            )
        )
    return parent_list


def add_child_input_to_parent(input_data, parent_input):
    for parent in parent_input:
        parent.children = []
        for item in input_data:
            if item.get("fhir_code_parent").get("value") in parent.fhir_code:
                parent.children.append(
                    ModelInput(
                        item.get("fhir_code_child").get("value"),
                        item.get("fhir_code_system_child").get("value"),
                        item.get("child_parameter").get("value"),
                        item.get("description_child").get("value", None),
                        None,
                        None,
                    )
                )
    return parent_input
