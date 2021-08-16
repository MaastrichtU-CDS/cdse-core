import uuid

from django.contrib.auth.models import User
from django.db import models

from datasource.models import FhirEndpoint


class PredictionModelSession(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    patient_id = models.CharField(max_length=64, null=False)
    secret_token = models.UUIDField(default=uuid.uuid4, editable=False)
    network_port = models.IntegerField(editable=False)
    image_name = models.CharField(max_length=2048, null=False)
    image_id = models.CharField(max_length=256, null=False)
    container_id = models.CharField(max_length=64, null=True, default=None)
    model_uri = models.CharField(max_length=2048, null=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    data_source = models.ForeignKey(FhirEndpoint, on_delete=models.SET_NULL, null=True)
    calculation_complete = models.BooleanField(default=False, null=False)
    error = models.TextField(null=True, default=None)


class PredictionModelData(models.Model):
    system = models.CharField(max_length=2048, null=False)
    code = models.CharField(max_length=64, null=False)
    input_parameter = models.CharField(max_length=2048, null=False)
    child_parameter = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(
        "PredictionModelSession", on_delete=models.CASCADE, null=True
    )


class PredictionModelResult(models.Model):
    system = models.CharField(max_length=2048, null=False)
    code = models.CharField(max_length=64, null=False)
    parameter = models.CharField(max_length=2048, null=False)
    parent_parameter = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    calculated_value = models.CharField(max_length=2048, null=True)
    session = models.ForeignKey(
        "PredictionModelSession", on_delete=models.CASCADE, null=True
    )
