from typing import List

from fhirclient import client
from fhirclient.models import observation
from fhirclient.models import patient
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

            return self._get_latest_observation(observation_list)
        except Exception:
            raise FhirEndpointFailedException()

    def get_patient_name_and_birthdate(self, patient_id):
        try:
            found_patient = patient.Patient.read(patient_id, self.smart.server)
            name = self.smart.human_name(found_patient.name[0])
            birthdate = found_patient.birthDate.isostring
            return {"name": name, "birthdate": birthdate}
        except Exception:
            raise FhirEndpointFailedException()

    @staticmethod
    def _get_latest_observation(observation_list):
        for outer_observation in observation_list:
            for inner_observations in observation_list:
                if (
                    outer_observation is not inner_observations
                    and outer_observation.code.coding[0].code
                    == inner_observations.code.coding[0].code
                    and outer_observation.code.coding[0].system
                    == inner_observations.code.coding[0].system
                    and outer_observation.effectiveDateTime.date
                    < inner_observations.effectiveDateTime.date
                ):
                    observation_list.remove(outer_observation)

        return observation_list
