import logging
import schedule
from django.utils import timezone
from datetime import timedelta

from dockerfacade.container import stop_container
from dockerfacade.exceptions import DockerEngineFailedException

from predictionmodel.models import PredictionModelSession
from django.db.models import Q


def remove_finished_containers():
    time_threshold = timezone.now() - timedelta(minutes=30)
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
        except DockerEngineFailedException as ex:
            logging.error("Exception stopping docker container: {}".format(ex))

        try:
            prediction_session.container_id = None
            prediction_session.save()
        except Exception as ex:
            logging.error("Exception: {}".format(ex))


# Configure jobs
schedule.every(10).minutes.do(remove_finished_containers)
