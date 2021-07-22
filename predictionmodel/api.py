import json
from django.urls import path

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from predictionmodel import tests


@api_view(["GET"])
def get_model_input(request):
    # Currently return test payload, next story this will be user selected input.
    return Response(tests.TEST_INPUT_PAYLOAD)


@api_view(["POST"])
def post_model_result(request):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    has_result_page = body.get("has_result_page")
    print(has_result_page)
    if has_result_page is None:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return Response(status=status.HTTP_200_OK)


urlpatterns = [
    path("ready", get_model_input, name="get_ready"),
    path("result", post_model_result, name="post_result"),
]
