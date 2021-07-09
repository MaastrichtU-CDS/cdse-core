from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="Api overview"),
    path("ready", views.ready, name="post call for when models is ready"),
    path("result", views.result, name="post call for prediction results"),
]
