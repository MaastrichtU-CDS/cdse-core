from django.urls import path, include


urlpatterns = [
    path("v1/", include("predictionmodel.api"), name="api_v1"),
]
