import uuid

from django.contrib.auth.models import User
from django.db import models

from predictionmodel.query.all_models import query_all_models
from utils.RDFQueryBuilder import query_form_string
from predictionmodel.query.execution_data import query_model_execution_data


def get_model_execution_data(selected_model_uri):
    query_string = query_model_execution_data(selected_model_uri)
    execution_data = query_form_string(query_string)

    docker_execution_data = [
        item
        for item in execution_data
        if "docker_execution" in str(item["exec_type"]["value"])
    ]
    return docker_execution_data[0]


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


class PredictionModelSession(models.Model):
    secret_token = models.UUIDField(default=uuid.uuid4, editable=False)
    network_port = models.IntegerField(editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
