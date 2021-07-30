from sparql.queryExecutor import query_form_string
from sparql.querys.all_models import query_all_models
from sparql.querys.execution_data import query_model_execution_data


def get_all_models():
    query_string = query_all_models()
    all_model_data = query_form_string(query_string)
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
    execution_data = query_form_string(query_string)

    docker_execution_data = [
        item
        for item in execution_data
        if "docker_execution" in str(item["exec_type"]["value"])
    ]
    return docker_execution_data[0]
