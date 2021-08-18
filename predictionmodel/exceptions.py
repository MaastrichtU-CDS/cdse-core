from rest_framework.exceptions import APIException


class InvalidInputException(Exception):
    """Indicating a required input parameter is missing."""

    def __init__(self, input_parameter):
        self.input_parameter = input_parameter


class NoPredictionModelSelectedException(Exception):
    """Indicating the required model uri is missing."""


class CannotSaveModelInputException(Exception):
    """Indicating some model inputs cannot be saved of linked to a session."""


class InvalidSessionTokenException(Exception):
    """Indicating the given Session Token is not valid."""


class CannotProcessModelOutputException(APIException):
    status_code = 422
    default_detail = "The given payload is either not compatible with the model description or invalid."
    default_code = "unprocessable entity"


class APIExceptionInvalidSessionToken(APIException):
    status_code = 403
    default_detail = (
        "Provided session token is not valid, please provide a valid token."
    )
    default_code = "forbidden"
