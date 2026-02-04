"""
Module: configuration_exception
Description:
    This module defines the ConfigurationException, a specialized application exception
    raised when the system configuration is invalid.
"""

from src.domain.exceptions.app_exception import AppException


class ConfigurationException(AppException):
    """
    Exception raised when an invalid configuration is detected.

    Inherits from AppException and uses the error code "CONFIG_ERROR".
    """

    def __init__(self, message: str):
        """
        Initializes the ConfigurationException with a custom error message.

        Args:
            message (str): Description of the configuration error.
        """
        super().__init__(message, code="CONFIG_ERROR")
