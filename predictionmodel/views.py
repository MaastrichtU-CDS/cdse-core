from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from dockerfacade.containerService import (
    prepare_container_properties,
    run_model_container,
)
from predictionmodel import constants
from predictionmodel.models import (
    PredictionModelSession,
    get_model_execution_data,
    get_all_models,
)


@method_decorator(login_required, name="dispatch")
class StartModelWizard(TemplateView):
    template_name = "prediction/start.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        try:
            context["prediction_models"] = get_all_models()
        except Exception as ex:
            messages.add_message(
                self.request, messages.ERROR, constants.ERROR_GET_MODEL_LIST_FAILED
            )

        return context


@method_decorator(login_required, name="dispatch")
class PrepareModelWizard(TemplateView):
    template_name = "prediction/prepare.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        patient_id = self.request.GET.get("patient_id")
        selected_model_uri = self.request.GET.get("selected_model_uri")

        if patient_id != "" or selected_model_uri != "":
            context["patient_id"] = patient_id
            context["selected_model_uri"] = selected_model_uri
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                constants.ERROR_REQUIRED_PARAMETERS_NOT_FOUND,
            )
        return context

    @staticmethod
    def post(request):
        selected_model_uri = request.POST["selected_model_uri"]
        if selected_model_uri != "":

            try:
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

                try:
                    run_model_container(*container_props.values())
                except Exception as ex:
                    messages.add_message(
                        request, messages.ERROR, constants.ERROR_PREDICTION_MODEL_FAILED
                    )

            except Exception as ex:
                messages.add_message(
                    request,
                    messages.ERROR,
                    constants.ERROR_GET_MODEL_DESCRIPTION_DETAILS_FAILED,
                )
        else:
            messages.add_message(
                request, messages.WARNING, constants.NO_PREDICTION_MODEL_SELECTED
            )
        return HttpResponseRedirect(".")
