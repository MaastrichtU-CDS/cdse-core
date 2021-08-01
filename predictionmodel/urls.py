from django.urls import path
from django.views.generic import RedirectView

from predictionmodel.views import StartModelWizard, PrepareModelWizard

urlpatterns = [
    path("", RedirectView.as_view(url='start/', permanent=True), name="prediction_index"),
    path("start/", StartModelWizard.as_view(), name="prediction_start"),
    path("prepare/", PrepareModelWizard.as_view(), name="prediction_prepare"),
]
