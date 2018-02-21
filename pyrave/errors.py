class PyRaveError(Exception):
    def __init__(self, message=None, http_status=None):
        super(PyRaveError, self).__init__(message)

        self.message = message
        self.http_status = http_status


class AuthKeyError(PyRaveError):
    """
    Auth Key Not Provided
    """
    pass


class HttpMethodError(PyRaveError):
    pass


class MissingParamError(PyRaveError):
    pass
