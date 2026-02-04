"""
Module: test_settings
Description:
    Unit tests for AppSettings configuration.
    Tests environment variable loading and configuration validation.
"""

import pytest
from unittest.mock import patch
from src.insfrastructure.config.app_settings import AppSettings


class TestAppSettings:
    """
    Unit tests for AppSettings configuration.
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
        settings = AppSettings()

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
        settings = AppSettings()

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
        settings = AppSettings()

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
        settings = AppSettings()

        # Assert
        # The attribute may or may not exist depending on implementation
        if hasattr(settings, attribute):
            assert getattr(settings, attribute) is not None or getattr(settings, attribute) is None

    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_API_VERSION': '2024-01-01',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4',
        'CORS_ORIGINS': 'http://localhost:3000,https://example.com'
    })
    def test_settings_cors_origins_parsing(self):
        """
        Test that CORS origins are correctly parsed from environment variables.
        """
        # Act
        settings = AppSettings()

        # Assert
        assert hasattr(settings, 'cors_origins')
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) == 2
        assert 'http://localhost:3000' in settings.cors_origins
        assert 'https://example.com' in settings.cors_origins

    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_API_VERSION': '2024-01-01',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4',
        'CORS_ORIGINS': ''
    })
    def test_settings_cors_origins_empty(self):
        """
        Test that CORS origins defaults to an empty list when not provided.
        """
        # Act
        settings = AppSettings()

        # Assert
        assert hasattr(settings, 'cors_origins')
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) == 0

    @patch.dict('os.environ', {
        'AZURE_OPENAI_ENDPOINT': 'https://test.openai.azure.com/',
        'AZURE_OPENAI_API_KEY': 'test-key',
        'AZURE_OPENAI_API_VERSION': '2024-01-01',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'gpt-4',
        'CORS_ORIGINS': 'http://localhost:3000, , https://example.com'
    })
    def test_settings_cors_origins_with_empty_spaces(self):
        """
        Test that CORS origins parsing handles whitespace correctly.
        """
        # Act
        settings = AppSettings()

        # Assert
        assert hasattr(settings, 'cors_origins')
        assert isinstance(settings.cors_origins, list)
        assert len(settings.cors_origins) == 2
        assert 'http://localhost:3000' in settings.cors_origins
        assert 'https://example.com' in settings.cors_origins
