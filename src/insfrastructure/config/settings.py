"""
Module: settings
Description:
    Centralized configuration for Azure OpenAI.
    Loads environment variables from a .env file and validates them.
"""

import os
from dotenv import load_dotenv


class AzureOpenAISettings:
    """
    Centralized configuration for Azure OpenAI.
    Reads environment variables from a .env file and performs basic validation.
    """

    def __init__(self):
        """
        Initializes the Azure OpenAI settings by reading environment variables
        and validating that all required settings are provided.
        """
        load_dotenv()
        self.endpoint: str = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.api_key: str = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.api_version: str = os.getenv("AZURE_OPENAI_API_VERSION", "")
        self.model: str = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")

        self._validate()

    def _validate(self):
        """
        Checks that all essential environment variables are present.

        Raises:
            ValueError: If any required environment variable is missing.
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
            raise ValueError(
                f"The following environment variables are missing: {', '.join(missing)}"
            )
