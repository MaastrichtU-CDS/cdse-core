import uuid
from datetime import timedelta
from django.test import TestCase
from unittest.mock import patch

from django.utils import timezone

from predictionmodel.models import PredictionModelSession
from predictionmodel.scheduler import remove_finished_containers


class TestSchedulerJob(TestCase):
    def setUp(self):
        self.uuid_one = uuid.uuid4()
        self.uuid_two = uuid.uuid4()
        self.uuid_three = uuid.uuid4()

        self.prediction_session_one = PredictionModelSession.objects.create(
            secret_token=self.uuid_one,
            network_port=1001,
            user=None,
            calculation_complete=True,
            container_id="123",
        )
        self.prediction_session_two = PredictionModelSession.objects.create(
            secret_token=self.uuid_two,
            network_port=1001,
            user=None,
            calculation_complete=False,
            container_id="345",
            error="error!",
        )
        self.prediction_session_three = PredictionModelSession.objects.create(
            secret_token=self.uuid_three,
            network_port=1001,
            user=None,
            calculation_complete=True,
            container_id="321",
        )

    @patch("predictionmodel.scheduler.stop_container")
    def test_remove_finished_containers(self, stop_container_mock):
        self.prediction_session_one.created_at = timezone.now() - timedelta(minutes=40)
        self.prediction_session_one.save()
        self.prediction_session_one.refresh_from_db()

        remove_finished_containers()

        prediction_sessions = PredictionModelSession.objects.filter(
            container_id__isnull=True
        )
        self.assertEqual(len(prediction_sessions), 2)
        self.assertEqual(prediction_sessions[0].secret_token, self.uuid_one)
        self.assertEqual(prediction_sessions[1].secret_token, self.uuid_two)
