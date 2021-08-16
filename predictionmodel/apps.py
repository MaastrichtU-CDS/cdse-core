import os

from django.apps import AppConfig


def startup():
    from predictionmodel.scheduler import run_scheduler

    run_scheduler()


class PredictionmodelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "predictionmodel"

    def ready(self):

        if os.environ.get("RUN_MAIN"):
            startup()
