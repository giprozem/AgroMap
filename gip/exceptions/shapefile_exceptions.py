import logging  # Import the logging module for error logging

from rest_framework.exceptions import APIException  # Import the base APIException class
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND  # Import HTTP status codes


# Custom exception class for a shapefile not found error
class ShapeFileNotFoundException(APIException):
    default_code = HTTP_400_BAD_REQUEST  # Set the default HTTP status code to 400 Bad Request
    default_detail = "Shapefile not found in the archive."  # Set a default error message


# Custom exception class for server alert with logging
class ServerAlertException(APIException):
    def __init__(self, detail=None, code=None, exception_message=None):
        super().__init__(detail, code)  # Call the constructor of the base APIException class
        # Log an error message with the "500 ERROR" label and the provided exception_message
        logging.exception("500 ERROR", exception_message)
