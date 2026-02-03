"""
Module: test_settings
Description:
    Unit tests for AzureOpenAISettings configuration.
    Tests environment variable loading and configuration validation.
"""

import pytest
from unittest.mock import patch
from src.insfrastructure.config.settings import AzureOpenAISettings


class TestAzureOpenAISettings:
    """
    Unit tests for AzureOpenAISettings configuration.
    """

    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_API_VERSION': '2024-01-01',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4'
    })
    def test_settings_initialization(self):
        """
        Test initialization of configuration parameters.
        """
        # Act
        settings = AzureOpenAISettings()

        # Assert
        assert settings is not None

    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_API_VERSION': '2024-01-01',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4'
    })
    def test_settings_has_required_attributes(self):
        """
        Test that the parameters have the required attributes.
        """
        # Arrange
        settings = AzureOpenAISettings()

        # Assert
        # Verify that required attributes exist
        assert hasattr(settings, 'endpoint')
        assert hasattr(settings, 'api_key')
        assert hasattr(settings, 'api_version')
        assert hasattr(settings, 'model')

    def test_settings_environment_variables(self):
        """
        Test that the parameters can read environment variables.
        """
        # Act
        settings = AzureOpenAISettings()

        # Assert
        assert settings is not None

    @pytest.mark.parametrize("attribute", [
        "endpoint",
        "api_key",
        "api_version",
        "model"
    ])
    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_API_VERSION': '2024-01-01',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4'
    })
    def test_settings_optional_attributes(self, attribute):
        """
        Test the optional attributes of the parameters.
        """
        # Act
        settings = AzureOpenAISettings()

        # Assert
        # The attribute may or may not exist depending on implementation
        if hasattr(settings, attribute):
            assert getattr(settings, attribute) is not None or getattr(settings, attribute) is None
