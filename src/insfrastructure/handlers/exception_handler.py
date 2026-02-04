"""
Module: fastapi_exception_handler
Description:
    This module provides a centralized exception handling service for FastAPI applications.
    It defines handlers for application-specific exceptions, validation errors, and
    generic unhandled exceptions, returning consistent JSON responses.
"""

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.domain.exceptions.app_exception import AppException


class FastAPIExceptionHandler:
    """
    Centralized exception handler for FastAPI.

    Provides static methods to handle:
        - Application-specific exceptions (AppException)
        - Request validation errors (RequestValidationError)
        - Generic unhandled exceptions (Exception)
    """

    @staticmethod
    async def handle_app_exception(request: Request, exc: AppException):
        """
        Handles custom application exceptions and returns a JSON response.

        Args:
            request (Request): The incoming FastAPI request.
            exc (AppException): The application-specific exception instance.

        Returns:
            JSONResponse: Response containing the error code and message.
                          HTTP status is 400 by default, or 500 for configuration errors.
        """
        return JSONResponse(
            status_code=400 if exc.code != "CONFIG_ERROR" else 500,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message
                }
            }
        )

    @staticmethod
    async def handle_validation_exception(request: Request, exc: RequestValidationError):
        """
        Handles request validation errors and returns a detailed JSON response.

        Args:
            request (Request): The incoming FastAPI request.
            exc (RequestValidationError): The validation exception raised by FastAPI.

        Returns:
            JSONResponse: Response containing the error code, a descriptive message,
                          and details of the validation errors. HTTP status is 422.
        """
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Data validation error: 'sentences' must be a list of strings",
                    "details": exc.errors()
                }
            }
        )

    @staticmethod
    async def handle_generic_exception(request: Request, exc: Exception):
        """
        Handles all other unhandled exceptions and returns a JSON response.

        Args:
            request (Request): The incoming FastAPI request.
            exc (Exception): The unhandled exception instance.

        Returns:
            JSONResponse: Response containing a generic internal server error code
                          and the exception message. HTTP status is 500.
        """
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": str(exc)
                }
            }
        )
