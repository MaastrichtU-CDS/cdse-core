from django.urls import path
from django.views.generic import RedirectView

from predictionmodel.views import (
    StartModelWizard,
    PrepareModelWizard,
    ResultWizard,
    LoadingWizard,
)

urlpatterns = [
    path(
        "", RedirectView.as_view(url="start/", permanent=True), name="prediction_index"
    ),
    path("start/", StartModelWizard.as_view(), name="prediction_start"),
    path("prepare/", PrepareModelWizard.as_view(), name="prediction_prepare"),
    path("loading/", LoadingWizard.as_view(), name="prediction_loading"),
    path("result/", ResultWizard.as_view(), name="prediction_result"),
]
