from django.urls import path

from predictionmodel.views import StartModelWizard, PrepareModelWizard

urlpatterns = [
    path("start/", StartModelWizard.as_view(), name="prediction_start"),
    path("prepare/", PrepareModelWizard.as_view(), name="prediction_prepare"),
]
