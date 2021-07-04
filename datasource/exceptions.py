class FHIRIncompatibleVersionException(Exception):
    """Indicating a unsupported version of fhir endpoints is used."""

    def __init__(self, version):
        self.version = version
