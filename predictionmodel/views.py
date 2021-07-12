import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from predictionmodel.client import Client


@api_view(["GET"])
def index(request):
    api_urls = {
        "ready": "/ready",
        "result": "/result",
        "stopped": "/stopped",
    }
    return Response(api_urls)


@api_view(["GET"])
def ready(request):
    Client().post_model_input()
    return Response()


@api_view(["POST"])
def result(request):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    print(body["has_result_page"])
    return Response()
