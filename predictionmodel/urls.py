from django.urls import path, include


urlpatterns = [
    path("v1/", include("predictionmodel.api_urls"), name="api version 1"),
]
