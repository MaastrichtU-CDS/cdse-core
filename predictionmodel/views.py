from typing import Any, Dict

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from predictionmodel import constants
from predictionmodel.client import PredictionModelClient


@method_decorator(login_required, name="dispatch")
class PrepareModelWizard(TemplateView):
    template_name = "prediction/start.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        try:
            context["prediction_models"] = PredictionModelClient.get_model_list()
        except Exception as ex:
            messages.add_message(
                self.request, messages.ERROR, constants.ERROR_GET_MODEL_LIST_FAILED
            )
        return context

    @staticmethod
    def post(request, *args, **kwargs):
        selected_model_id = request.POST["select_model_id"]
        if selected_model_id == "":
            messages.add_message(
                request, messages.WARNING, constants.NO_PREDICTION_MODEL_SELECTED
            )
        return HttpResponseRedirect(".")
