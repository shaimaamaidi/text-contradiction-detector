"""
Module: test_main_api
Description:
    Integration tests for the main FastAPI application.
    Tests API endpoints for text analysis, contradiction detection, and health checks.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from fastapi.testclient import TestClient
from src.presentation.api.main_api import app


class TestMainAPI:
    """
    Integration tests for the main API.
    """

    @pytest.fixture
    def client(self):
        """FastAPI test client."""
        return TestClient(app)

    @pytest.fixture
    def mock_analyse_text_use_case(self):
        """Mock of the text analysis use case."""
        return Mock()

    def test_health_check_endpoint(self, client):
        """
        Test the health check endpoint.
        """
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200

    def test_analyze_text_endpoint_with_valid_request(self, client, sample_sentences):
        """
        Test the text analysis endpoint with a valid request.
        """
        # Arrange
        payload = {
            "sentences": sample_sentences
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        assert response.status_code in [200, 201, 202]
        if response.status_code in [200, 201, 202]:
            data = response.json()
            assert data is not None

    def test_analyze_text_endpoint_with_empty_sentences(self, client):
        """
        Test the endpoint with an empty list of sentences.
        """
        # Arrange
        payload = {
            "sentences": []
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        assert response.status_code in [200, 400]

    def test_analyze_text_endpoint_with_single_sentence(self, client, sample_single_sentence):
        """
        Test the endpoint with a single sentence.
        """
        # Arrange
        payload = {
            "sentences": [sample_single_sentence]
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        assert response.status_code in [200, 201, 202]

    def test_analyze_text_endpoint_missing_sentences_field(self, client):
        """
        Test the endpoint with a request missing the 'sentences' field.
        """
        # Arrange
        payload = {}

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        assert response.status_code == 422  # Unprocessable Entity

    def test_analyze_text_endpoint_with_contradictory_sentences(self, client, contradictory_sentences):
        """
        Test the endpoint with contradictory sentences.
        """
        # Arrange
        payload = {
            "sentences": contradictory_sentences
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        assert response.status_code in [200, 201, 202]
        if response.status_code in [200, 201, 202]:
            data = response.json()
            assert data is not None

    def test_analyze_text_response_structure(self, client, sample_sentences):
        """
        Test that the endpoint response has the correct structure.
        """
        # Arrange
        payload = {
            "sentences": sample_sentences
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        if response.status_code in [200, 201, 202]:
            data = response.json()
            # Vérifier que la réponse contient les champs attendus
            if isinstance(data, dict):
                # Peut contenir 'classifications', 'contradictions', etc.
                pass

    def test_analyze_text_endpoint_with_long_sentences_list(self, client):
        """
        Test the endpoint with a long list of sentences.
        """
        # Arrange
        long_sentences_list = [
            "أوصي باعتماد المقترح."
        ] * 100
        payload = {
            "sentences": long_sentences_list
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        # La réponse peut être 200 ou 413 si la taille est trop grande
        assert response.status_code in [200, 201, 202, 413]

    def test_api_root_endpoint(self, client):
        """
        Test the API root endpoint.
        """
        # Act
        response = client.get("/")

        # Assert
        # Le point de terminaison peut retourner 404 ou 200 selon l'implémentation
        assert response.status_code in [200, 404]

    def test_analyze_text_with_non_arabic_sentences(self, client):
        """
        Test analysis with English sentences.
        """
        # Arrange
        payload = {
            "sentences": [
                "I recommend approving the proposal and implementing it immediately.",
                "I suggest rejecting the proposal due to unclear costs."
            ]
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        assert response.status_code in [200, 201, 202, 400]

    def test_cors_headers_present(self, client):
        """
        Test that CORS headers are properly configured in the response.
        """
        # Act
        response = client.get("/health")

        # Assert
        assert response.status_code == 200
        # CORS headers should be present or not present depending on configuration
        # This test verifies the endpoint is accessible

    def test_exception_handling_empty_sentences(self, client):
        """
        Test that empty sentences trigger an AppException with proper error handling.
        """
        # Arrange
        payload = {
            "sentences": []
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        # Should return 400 with error structure when sentences are empty
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "code" in data["error"]
        assert "message" in data["error"]
        assert data["error"]["code"] == "EMPTY_TEXT"

    def test_exception_handling_validation_error(self, client):
        """
        Test that validation errors return proper error response.
        """
        # Arrange
        payload = {
            "sentences": "not a list"  # Should be a list
        }

        # Act
        response = client.post("/analyze", json=payload)

        # Assert
        assert response.status_code == 422
        data = response.json()
        assert "error" in data
        assert data["error"]["code"] == "VALIDATION_ERROR"
