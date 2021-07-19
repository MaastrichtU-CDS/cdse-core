import json

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from predictionmodel.client import Client


@api_view(["GET"])
def ready(request):
    Client().post_model_input()
    return Response(status=status.HTTP_200_OK)


@api_view(["POST"])
def result(request):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    has_result_page = body.get("has_result_page")

    if has_result_page is None:
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    else:
        return Response(status=status.HTTP_200_OK)
