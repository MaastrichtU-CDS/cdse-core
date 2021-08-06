from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from datasource.models import FhirEndpoint
from dockerfacade.container import (
    prepare_container_properties,
    run_model_container,
)
from dockerfacade.exceptions import DockerEngineFailedException
from fhir.exceptions import FhirEndpointFailedException
from fhir.client import Client as FhirClient
from predictionmodel import constants
from predictionmodel.exceptions import (
    InvalidInputException,
    NoPredictionModelSelectedException,
)
from predictionmodel.models import PredictionModelSession
from sparql.exceptions import SparqlQueryFailedException
from sparql.query import get_all_models, get_model_execution_data, get_model_input_data


@method_decorator(login_required, name="dispatch")
class StartModelWizard(TemplateView):
    template_name = "prediction/start.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["fhir_endpoints"] = FhirEndpoint.objects.all()

        try:
            context["prediction_models"] = get_all_models()
        except SparqlQueryFailedException:
            messages.add_message(
                self.request, messages.ERROR, constants.ERROR_GET_MODEL_LIST_FAILED
            )

        return context


@method_decorator(login_required, name="dispatch")
class PrepareModelWizard(TemplateView):
    template_name = "prediction/prepare.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        fhir_endpoint_id = self.request.GET.get("fhir_endpoint_id")
        patient_id = self.request.GET.get("patient_id")
        selected_model_uri = self.request.GET.get("selected_model_uri")

        try:
            if patient_id == "" or patient_id is None:
                raise InvalidInputException("patient_id")

            if selected_model_uri == "" or selected_model_uri is None:
                raise InvalidInputException("selected_model_uri")

            if fhir_endpoint_id == "" or fhir_endpoint_id is None:
                fhir_endpoint_id = FhirEndpoint.get_default_id_or_none()
                if fhir_endpoint_id is None:
                    raise InvalidInputException("fhir_endpoint_id")

            fhir_endpoint_url = FhirEndpoint.get_full_url_by_id(fhir_endpoint_id)
            context["patient_information"] = FhirClient(
                fhir_endpoint_url
            ).get_patient_name_and_birthdate(patient_id)

            patient_observations = FhirClient(
                fhir_endpoint_url
            ).get_patient_observations(patient_id)

            model_input_list = get_model_input_data(selected_model_uri)
            context["model_input_list"] = match_input_with_observations(
                model_input_list, patient_observations
            )

        except InvalidInputException as ex:
            messages.add_message(
                self.request,
                messages.ERROR,
                constants.ERROR_REQUIRED_INPUT_NOT_FOUND + ex.input_parameter,
            )
        except FhirEndpointFailedException:
            messages.add_message(
                self.request,
                messages.ERROR,
                constants.ERROR_GET_DATA_FROM_FHIR_FAILED,
            )
        except Exception:
            messages.add_message(
                self.request,
                messages.ERROR,
                constants.ERROR_UNKNOWN,
            )

        context["selected_model_uri"] = selected_model_uri
        return context

    @staticmethod
    def post(request):
        selected_model_uri = request.POST["selected_model_uri"]

        try:
            if selected_model_uri == "" or selected_model_uri is None:
                raise NoPredictionModelSelectedException()
            docker_execution_data = get_model_execution_data(selected_model_uri)
            container_props = prepare_container_properties(
                docker_execution_data.get("image_name").get("value"),
                docker_execution_data.get("image_id").get("value"),
            )
            PredictionModelSession.objects.create(
                secret_token=container_props.get("secret_token"),
                network_port=container_props.get("port"),
                user=request.user,
            )
            run_model_container(*container_props.values())
        except DockerEngineFailedException:
            messages.add_message(
                request, messages.ERROR, constants.ERROR_PREDICTION_MODEL_FAILED
            )
        except SparqlQueryFailedException:
            messages.add_message(
                request,
                messages.ERROR,
                constants.ERROR_GET_MODEL_DESCRIPTION_DETAILS_FAILED,
            )
        except NoPredictionModelSelectedException:
            messages.add_message(
                request, messages.ERROR, constants.NO_PREDICTION_MODEL_SELECTED
            )
        except Exception:
            messages.add_message(
                request,
                messages.ERROR,
                constants.ERROR_UNKNOWN,
            )

        return HttpResponseRedirect("/admin")


def match_input_with_observations(input_parameters, observations_list):
    for input_item in input_parameters:
        for observation_item in observations_list:
            if (
                observation_item.valueCodeableConcept is not None
                and observation_item.code is not None
            ):
                if (
                    observation_item.code.coding[0].system
                    == input_item["input_type_parent"]
                    and observation_item.code.coding[0].code
                    == input_item["code_parent"]
                ):
                    for child_parameter in input_item["child_values"]:
                        if (
                            child_parameter["input_type_child"]
                            == observation_item.valueCodeableConcept.coding[0].system
                            and child_parameter["code_child"]
                            == observation_item.valueCodeableConcept.coding[0].code
                        ):
                            input_item["matching_child_input"] = child_parameter
    return input_parameters
