"""
Module: settings
Description:
    Centralized configuration management for Azure OpenAI.
    Loads environment variables from a .env file and validates that all required settings are provided.
    Includes configuration for CORS (Cross-Origin Resource Sharing) to control which origins can access the API.
"""

import os
from dotenv import load_dotenv

from src.domain.exceptions.configuration_exception import ConfigurationException


class AppSettings:
    """
    Centralized configuration for Azure OpenAI.

    Reads environment variables from a .env file and performs basic validation.
    Provides the following attributes:
        - cors_origins (List[str]): List of allowed origins for CORS.
        - endpoint (str): Azure OpenAI endpoint URL.
        - api_key (str): API key for Azure OpenAI.
        - api_version (str): Version of the Azure OpenAI API.
        - model (str): Deployment/model name used for OpenAI requests.
    """

    def __init__(self):
        """
        Initializes the Azure OpenAI settings by reading environment variables
        and validating them.

        This includes reading the following:
            - AZURE_OPENAI_ENDPOINT
            - AZURE_OPENAI_API_KEY
            - AZURE_OPENAI_API_VERSION
            - AZURE_OPENAI_DEPLOYMENT_NAME
            - CORS_ORIGINS (a comma-separated list of allowed origins for CORS)

        Raises:
            ConfigurationException: If any required environment variable is missing.
        """
        load_dotenv()

        cors_origins_str = os.getenv("CORS_ORIGINS", "")
        if cors_origins_str:
            self.cors_origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]
        else:
            self.cors_origins = []

        self.endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "")
        self.model: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")

        self._validate()

    def _validate(self):
        """
        Validates that all essential environment variables are present.

        Raises:
            ConfigurationException: If any required environment variable is missing.
        """
        if not all([self.endpoint, self.api_key, self.api_version, self.model]):
            missing = [
                name
                for name, value in [
                    ("AZURE_OPENAI_ENDPOINT", self.endpoint),
                    ("AZURE_OPENAI_API_KEY", self.api_key),
                    ("AZURE_OPENAI_API_VERSION", self.api_version),
                    ("AZURE_OPENAI_DEPLOYMENT_NAME", self.model),
                ]
                if not value
            ]
            raise ConfigurationException(
                f"The following environment variables are missing: {', '.join(missing)}"
            )
