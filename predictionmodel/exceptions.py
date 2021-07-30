class InvalidInputException(Exception):
    """Indicating a required input parameter is missing."""

    def __init__(self, input_parameter):
        self.input_parameter = input_parameter


class NoPredictionModelSelectedException(Exception):
    """Indicating the required model uri is missing."""
