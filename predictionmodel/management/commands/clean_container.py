import time
import schedule
from django.core.management import BaseCommand

from predictionmodel.scheduler import remove_finished_containers


class Command(BaseCommand):
    help = "Clean the running docker containers after finishing predictions"

    def handle(self, *args, **options):
        schedule.every(10).minutes.do(remove_finished_containers)

        while True:
            schedule.run_pending()
            time.sleep(10)
