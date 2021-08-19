import os
from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from datasource.models import FhirEndpoint
from dockerfacade.container import (
    prepare_container_properties,
    run_container,
)
from dockerfacade.exceptions import DockerEngineFailedException
from fhir.exceptions import FhirEndpointFailedException
from fhir.client import Client as FhirClient
from predictionmodel import constants
from predictionmodel.constants import (
    ERROR_PREDICTION_CALCULATION,
    WARNING_SESSION_ENDED,
)
from predictionmodel.exceptions import (
    InvalidInputException,
    NoPredictionModelSelectedException,
    CannotSaveModelInputException,
    InvalidSessionTokenException,
)
from predictionmodel.models import (
    PredictionModelSession,
    PredictionModelData,
    PredictionModelResult,
)
from sparql.exceptions import SparqlQueryFailedException
from sparql.query import (
    get_all_models,
    get_model_execution_data,
    get_model_input_data,
    get_model_output_data,
)


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

        fhir_endpoint_id = self.request.GET.get("fhir_endpoint_id", None)
        patient_id = self.request.GET.get("patient_id", None)
        selected_model_uri = self.request.GET.get("selected_model_uri", None)

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
        context["patient_id"] = patient_id
        context["fhir_endpoint_id"] = fhir_endpoint_id
        return context

    def post(self, request):
        selected_model_uri = request.POST.get("selected_model_uri", None)
        fhir_endpoint_id = request.POST.get("fhir_endpoint_id", None)
        patient_id = request.POST.get("patient_id", None)

        try:
            if selected_model_uri == "" or selected_model_uri is None:
                raise NoPredictionModelSelectedException()

            if patient_id == "" or patient_id is None:
                raise InvalidInputException("patient_id")

            if fhir_endpoint_id == "" or fhir_endpoint_id is None:
                raise InvalidInputException("fhir_endpoint_id")

            prediction_session, container_properties = create_prediction_session(
                selected_model_uri, patient_id, fhir_endpoint_id, request.user
            )

            save_prediction_input(request.POST, selected_model_uri, prediction_session)

            container = run_container(
                prediction_session.image_name,
                prediction_session.image_id,
                prediction_session.network_port,
                prediction_session.secret_token,
                container_properties.get("invocation_url"),
            )

            prediction_session.container_id = container.id
            prediction_session.save()

            return redirect(
                reverse("prediction_loading")
                + "?session_token="
                + str(prediction_session.secret_token)
            )

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
        except CannotSaveModelInputException:
            messages.add_message(
                request, messages.ERROR, constants.ERROR_INPUT_DATA_SAVE_FAILED
            )
        except InvalidInputException as ex:
            messages.add_message(
                self.request,
                messages.ERROR,
                constants.ERROR_REQUIRED_INPUT_NOT_FOUND + ex.input_parameter,
            )
        except Exception:
            messages.add_message(
                request,
                messages.ERROR,
                constants.ERROR_UNKNOWN,
            )
        return redirect("prediction_start")


def match_input_with_observations(input_parameters, observations_list):
    for input_item in input_parameters:
        for observation_item in observations_list:
            if (
                observation_item.valueCodeableConcept is not None
                and observation_item.code is not None
            ):
                if (
                    observation_item.code.coding[0].system
                    == input_item.fhir_code_system
                    and observation_item.code.coding[0].code == input_item.fhir_code
                ):
                    for child in input_item.children:
                        if (
                            observation_item.valueCodeableConcept.coding[0].system
                            == child.fhir_code_system
                            and observation_item.valueCodeableConcept.coding[0].code
                            == child.fhir_code
                        ):
                            input_item.matched_child = child
    return input_parameters


def create_prediction_session(selected_model_uri, patient_id, fhir_endpoint_id, user):
    docker_execution_data = get_model_execution_data(selected_model_uri)
    container_props = prepare_container_properties(
        docker_execution_data.get("image_name").get("value"),
        docker_execution_data.get("image_id").get("value"),
    )

    try:
        prediction_session = PredictionModelSession.objects.create(
            patient_id=patient_id,
            data_source=FhirEndpoint.objects.get(id=fhir_endpoint_id),
            secret_token=container_props.get("secret_token"),
            network_port=container_props.get("port"),
            image_name=container_props.get("image_name"),
            image_id=container_props.get("image_id"),
            model_uri=selected_model_uri,
            user=user,
        )

        return prediction_session, container_props

    except Exception:
        raise CannotSaveModelInputException()


def save_prediction_input(post_data, selected_model_uri, prediction_session):
    model_input_list = get_model_input_data(selected_model_uri)

    for parent_model_input in model_input_list:
        try:
            fhir_code_child = post_data.get(parent_model_input.fhir_code, "")
            fhir_code_child_override = post_data.get(
                parent_model_input.fhir_code + "-override", ""
            )

            if fhir_code_child_override != "":
                fhir_code_child = fhir_code_child_override

            if fhir_code_child == "":
                pass

            child = parent_model_input.get_child_by_code(fhir_code_child)

            model_input_data_child = PredictionModelData.objects.create(
                system=child.fhir_code_system,
                code=child.fhir_code,
                input_parameter=child.parameter,
                child_parameter=None,
            )

            PredictionModelData.objects.create(
                system=parent_model_input.fhir_code_system,
                code=parent_model_input.fhir_code,
                input_parameter=parent_model_input.parameter,
                child_parameter=model_input_data_child,
                session=prediction_session,
            )
        except Exception:
            raise CannotSaveModelInputException()


@method_decorator(login_required, name="dispatch")
class LoadingWizard(TemplateView):
    template_name = "prediction/loading.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        secret_token = self.request.GET.get("session_token", "")

        try:
            context["prediction_session"] = _get_prediction_session(secret_token)
            context["error_message"] = ERROR_PREDICTION_CALCULATION

        except InvalidSessionTokenException:
            messages.add_message(
                self.request,
                messages.ERROR,
                constants.ERROR_PROVIDED_SESSION_TOKEN_INVALID,
            )
        except Exception:
            messages.add_message(self.request, messages.ERROR, constants.ERROR_UNKNOWN)

        return context


@method_decorator(login_required, name="dispatch")
class ResultWizard(TemplateView):
    template_name = "prediction/result.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        secret_token = self.request.GET.get("session_token", "")

        try:
            prediction_session = _get_prediction_session(secret_token)

            output_data_list = get_model_output_data(prediction_session.model_uri)
            parent_results = prediction_session.predictionmodelresult_set.filter(
                parent_parameter__isnull=True
            )

            child_results = []
            for parent_item in parent_results:
                child_list = PredictionModelResult.objects.filter(
                    parent_parameter=parent_item
                )
                for child in child_list:
                    child_results.append(child)

            context["output_data_list"] = output_data_list
            context["parent_results"] = parent_results
            context["child_results"] = child_results
            context["prediction_session"] = prediction_session
            context["warning_session_ended"] = WARNING_SESSION_ENDED
            context["invocation_host"] = os.environ.get("INVOCATION_HOST", "localhost")

        except (ObjectDoesNotExist, InvalidSessionTokenException):
            messages.add_message(
                self.request,
                messages.ERROR,
                constants.ERROR_PROVIDED_SESSION_TOKEN_INVALID,
            )

        except Exception:
            messages.add_message(self.request, messages.ERROR, constants.ERROR_UNKNOWN)

        return context


def _get_prediction_session(secret_token):
    if secret_token == "" or secret_token is None:
        raise InvalidSessionTokenException()

    return PredictionModelSession.objects.get(secret_token=secret_token)
