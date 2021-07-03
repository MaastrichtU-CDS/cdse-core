from django.contrib import admin
from datasource.models import FhirEndpoint


class FhirEndpointAdmin(admin.ModelAdmin):
    list_display = ("name", "full_url", "is_default")
    search_fields = ("name", "full_url")
    pass


admin.site.register(FhirEndpoint, FhirEndpointAdmin)
