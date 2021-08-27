class FhirEndpointFailedException(Exception):
    """Indicating fhir endpoint is not working."""

    def __init__(self, message):
        self.message = message
