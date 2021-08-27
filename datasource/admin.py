import logging

from django.contrib import admin
from django.http import HttpResponseRedirect
from fhirclient import client
from fhirclient.models import capabilitystatement

from datasource import constants
from datasource.models import FhirEndpoint, FHIRIncompatibleVersionException
from django.contrib import messages


class FhirEndpointAdmin(admin.ModelAdmin):
    change_form_template = "datasource/change_form.html"
    list_display = ("name", "full_url", "is_default")
    search_fields = ("name", "full_url")

    def response_change(self, request, form_obj):
        if "_test" in request.POST:

            fhir_client = client.FHIRClient(
                settings={"app_id": form_obj.name, "api_base": form_obj.full_url}
            )

            try:
                fhir_client.prepare()
                meta_resp = capabilitystatement.CapabilityStatement.read_from(
                    "metadata", fhir_client.server
                )
                FhirEndpoint.supported_version_check(meta_resp.fhirVersion)

            except FHIRIncompatibleVersionException as ex:
                logging.warning("Incompatible FHIR version exception: {}".format(ex))
                messages.add_message(
                    request,
                    messages.WARNING,
                    constants.TEST_ERROR_VERSION,
                )
                return HttpResponseRedirect(".")

            except Exception as ex:
                if (
                    hasattr(ex, "response")
                    and hasattr(ex.response, "status_code")
                    and ex.response.status_code
                    in [
                        401,
                        403,
                        404,
                    ]
                ):
                    if ex.response.status_code == 401:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            constants.TEST_ERROR_401,
                        )
                    if ex.response.status_code == 403:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            constants.TEST_ERROR_403,
                        )
                    if ex.response.status_code == 404:
                        messages.add_message(
                            request,
                            messages.ERROR,
                            constants.TEST_ERROR_404,
                        )
                else:
                    logging.warning("Tested FHIR-endpoint exception: {}".format(ex))
                    messages.add_message(
                        request, messages.ERROR, constants.TEST_ERROR_UNKNOWN
                    )
                return HttpResponseRedirect(".")

            messages.add_message(request, messages.INFO, constants.TEST_SUCCESS)
            return HttpResponseRedirect(".")
        return super().response_change(request, form_obj)


admin.site.register(FhirEndpoint, FhirEndpointAdmin)
