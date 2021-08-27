import json

from django.urls import path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from predictionmodel.exceptions import (
    CannotProcessModelOutputException,
    APIExceptionInvalidSessionToken,
)
from predictionmodel.models import PredictionModelSession, PredictionModelResult
from sparql.query import get_model_output_data


@api_view(["GET"])
def get_model_input(request):
    prediction_session = _get_prediction_session(request)

    payload = {}
    for model_input in prediction_session.predictionmodeldata_set.all():
        payload[
            model_input.input_parameter
        ] = model_input.child_parameter.input_parameter

    return Response(payload)


@api_view(["POST"])
def post_model_result(request):
    prediction_session = _get_prediction_session(request)

    try:
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        output_data_list = get_model_output_data(prediction_session.model_uri)
        advanced_view = body.get("has_result_page", False)

        for output_item in output_data_list:
            parent_result_item = body.get(output_item.parameter)

            parent = PredictionModelResult.objects.create(
                system=output_item.fhir_code_system,
                code=output_item.fhir_code,
                parameter=output_item.parameter,
                calculated_value=None,
                parent_parameter=None,
                session=prediction_session,
            )

            for output_item_child in output_item.children:
                calculated_value = parent_result_item.get(output_item_child.parameter)
                PredictionModelResult.objects.create(
                    system=output_item_child.fhir_code_system,
                    code=output_item_child.fhir_code,
                    parameter=output_item_child.parameter,
                    calculated_value=calculated_value,
                    parent_parameter=parent,
                    session=None,
                )
        prediction_session.calculation_complete = True
        prediction_session.advanced_view = advanced_view
        prediction_session.save()
        return Response(status=status.HTTP_200_OK)

    except Exception:
        CannotProcessModelOutputException()
        prediction_session.error = CannotProcessModelOutputException.default_detail
        prediction_session.save()


@api_view(["GET"])
def check_calculation_complete(request):
    prediction_session = _get_prediction_session(request)
    return Response(
        data={
            "calculation_complete": prediction_session.calculation_complete,
            "error": prediction_session.error,
        }
    )


@api_view(["POST"])
def post_calculation_error(request):
    prediction_session = _get_prediction_session(request)

    try:
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        error_message = body.get("error_message", "")
        prediction_session.error = error_message
        prediction_session.save()
        return Response(status=status.HTTP_200_OK)
    except Exception:
        APIException()


def _get_prediction_session(request):
    secret_token = request.META.get("HTTP_AUTHORIZATION", "")
    if secret_token == "" or secret_token is None:
        raise APIExceptionInvalidSessionToken()

    try:
        prediction_session = PredictionModelSession.objects.get(
            secret_token=secret_token, container_id__isnull=False
        )
        return prediction_session

    except Exception:
        raise APIExceptionInvalidSessionToken()


urlpatterns = [
    path("ready", get_model_input, name="get_model_input"),
    path("result", post_model_result, name="post_result"),
    path("check", check_calculation_complete, name="check_result"),
    path("error", post_calculation_error, name="calculation_error"),
]
