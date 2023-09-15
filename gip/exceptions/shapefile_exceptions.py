import logging

from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class ShapeFileNotFoundException(APIException):
    default_code = HTTP_400_BAD_REQUEST
    default_detail = "Shapefile not found in the archive."


class ServerAlertException(APIException):
    def __init__(self, detail=None, code=None, exception_message=None):
        super().__init__(detail, code)
        logging.exception("500 ERROR", exception_message)


