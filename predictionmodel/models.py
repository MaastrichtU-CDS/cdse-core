import uuid

from django.contrib.auth.models import User
from django.db import models


class PredictionModelSession(models.Model):
    secret_token = models.UUIDField(default=uuid.uuid4, editable=False)
    network_port = models.IntegerField(editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
