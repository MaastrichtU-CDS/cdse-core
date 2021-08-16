import os
import threading
import time
import schedule
from django.utils import timezone
from datetime import timedelta

from dockerfacade.container import stop_container
from dockerfacade.exceptions import DockerEngineFailedException
from predictionmodel.constants import (
    ERROR_STOPPING_CONTAINER,
    ERROR_CHANGING_PREDICTION_MODEL_CONTAINER_ID,
)
from predictionmodel.models import PredictionModelSession
from django.db.models import Q


def run_scheduler(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def remove_finished_containers():
    time_threshold = timezone.now() - timedelta(
        minutes=os.environ.get("CONTAINER_LIFETIME_MINUTES", 30)
    )
    prediction_sessions = PredictionModelSession.objects.filter(
        Q(
            created_at__lt=time_threshold,
            calculation_complete=True,
            container_id__isnull=False,
        )
        | Q(container_id__isnull=False, error__isnull=False)
    )

    for prediction_session in prediction_sessions:
        try:
            stop_container(prediction_session.container_id)
        except DockerEngineFailedException:
            print(ERROR_STOPPING_CONTAINER)

        try:
            prediction_session.container_id = None
            prediction_session.save()
        except Exception:
            print(ERROR_CHANGING_PREDICTION_MODEL_CONTAINER_ID)


# Configure jobs
schedule.every(10).minutes.do(remove_finished_containers)
