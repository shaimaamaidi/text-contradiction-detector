"""
Module: app_exception
Description:
    This module defines the base application exception (AppException) used for
    domain-specific or business logic errors. Other custom exceptions should inherit from this class.
"""


class AppException(Exception):
    """
    Base application (business) exception.

    Attributes:
        message (str): Description of the exception.
        code (str): Error code representing the type of application exception. Defaults to "APP_ERROR".
    """

    def __init__(self, message: str, code: str = "APP_ERROR"):
        """
        Initializes the AppException with a message and an optional error code.

        Args:
            message (str): Description of the exception.
            code (str, optional): Specific error code for the exception. Defaults to "APP_ERROR".
        """
        self.message = message
        self.code = code
        super().__init__(message)
