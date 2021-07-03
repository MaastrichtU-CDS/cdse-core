from django.core.exceptions import ValidationError
from django.db import models


class FhirEndpoint(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=350)
    full_url = models.URLField(
        max_length=2048, null=False, default="http://localhost:1234/fhir"
    )
    is_default = models.BooleanField(default=False)

    def clean(self):
        if self.is_default:
            active = FhirEndpoint.objects.filter(is_default=True)
            if active.exists():
                raise ValidationError(
                    "An other endpoint is default, please disable that one first"
                )
