from django.core.exceptions import ValidationError
from django.db import models

from datasource.exceptions import FHIRIncompatibleVersionException


class FhirEndpoint(models.Model):
    supported_major_versions = ["4"]

    name = models.CharField(max_length=80, unique=True)
    description = models.CharField(max_length=350)
    full_url = models.URLField(
        max_length=2048, null=False, default="http://localhost:1234/fhir"
    )
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def clean(self):
        if self.is_default:
            active = FhirEndpoint.objects.filter(is_default=True).exclude(pk=self.pk)
            if active.exists():
                raise ValidationError(
                    "An other endpoint is default, please disable that one first"
                )

    @staticmethod
    def supported_version_check(found_version: str) -> bool:
        major_version = found_version.split(".")[0]

        if major_version not in FhirEndpoint.supported_major_versions:
            raise FHIRIncompatibleVersionException(major_version)
        pass
