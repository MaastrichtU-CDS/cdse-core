from django.urls import path

from predictionmodel.views import PrepareModelWizard

urlpatterns = [path("start/", PrepareModelWizard.as_view(), name="prediction_start")]
