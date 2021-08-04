from typing import List

from fhirclient import client
from fhirclient.models import observation

from fhir.exceptions import FhirEndpointFailedException


class Client:
    smart = None

    def __init__(self, fhir_url):
        settings = {"app_id": "my_web_app", "api_base": fhir_url}

        self.smart = client.FHIRClient(settings=settings)

    def get_patient_observations(self, patient_id):
        try:
            observation_list: List[
                observation.Observation
            ] = observation.Observation.where(
                struct={"patient": patient_id}
            ).perform_resources(
                self.smart.server
            )
            return observation_list
        except Exception:
            raise FhirEndpointFailedException()
