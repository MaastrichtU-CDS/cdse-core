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
                "ncit_parent": item.get("ncit_parent").get("value"),
                "parent_input_parameter": item.get("parent_input_parameter").get(
                    "value"
                ),
            }
        )
    return list({item["ncit_parent"]: item for item in parent_list}.values())


def add_child_input_to_parent(input_data, parent_input):
    for parent in parent_input:
        parent["child_values"] = []
        for item in input_data:
            if item.get("ncit_parent").get("value") in parent["ncit_parent"]:
                parent["child_values"].append(
                    {
                        "ncit_child": item.get("ncit_child").get("value"),
                        "model_input_parameter": item.get("model_input_parameter").get(
                            "value"
                        ),
                    }
                )
    return parent_input
