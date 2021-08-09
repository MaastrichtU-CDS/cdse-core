import uuid

from django.contrib.auth.models import User
from django.db import models


class PredictionModelSession(models.Model):
    secret_token = models.UUIDField(default=uuid.uuid4, editable=False)
    network_port = models.IntegerField(editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class PredictionModelData(models.Model):
    system = models.CharField(max_length=2048, null=False)
    code = models.CharField(max_length=64, null=False)
    input_parameter = models.CharField(max_length=2048, null=False)
    child_parameter = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    session = models.ForeignKey(
        "PredictionModelSession", on_delete=models.CASCADE, null=True
    )
