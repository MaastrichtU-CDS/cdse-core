from . import views
from django.urls import path

urlpatterns = [
    path("ready", views.ready, name="get_ready"),
    path("result", views.result, name="post_result"),
]
