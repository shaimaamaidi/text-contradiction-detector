"""
Module: test_dtos
Description:
    Unit tests for Data Transfer Objects (DTOs).
    Tests AnalysisRequest and AnalysisResponse serialization and structure.
"""

import pytest
from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse


class TestAnalysisRequest:
    """
    Unit tests for the AnalysisRequest DTO.
    """

    def test_analysis_request_creation(self, sample_sentences):
        """
        Test creation of an AnalysisRequest instance.
        """
        # Act
        request = AnalysisRequest(sentences=sample_sentences)

        # Assert
        assert request is not None
        assert request.sentences == sample_sentences
        assert len(request.sentences) == len(sample_sentences)

    def test_analysis_request_with_single_sentence(self, sample_single_sentence):
        """
        Test creation with a single sentence.
        """
        # Act
        request = AnalysisRequest(sentences=[sample_single_sentence])

        # Assert
        assert len(request.sentences) == 1
        assert request.sentences[0] == sample_single_sentence

    def test_analysis_request_with_empty_list(self, empty_sentences):
        """
        Test creation with an empty list.
        """
        # Act
        request = AnalysisRequest(sentences=empty_sentences)

        # Assert
        assert len(request.sentences) == 0

    def test_analysis_request_serialization(self, sample_sentences):
        """
        Test serialization of the DTO to JSON.
        """
        # Arrange
        request = AnalysisRequest(sentences=sample_sentences)

        # Act
        if hasattr(request, 'dict'):
            data = request.dict()
            assert "sentences" in data
            assert data["sentences"] == sample_sentences


class TestAnalysisResponse:
    """
    Unit tests for the AnalysisResponse DTO.
    """

    def test_analysis_response_creation(self):
        """
        Test creation of an AnalysisResponse instance.
        """
        # Arrange
        categories = [
            {
                "category_name": "support",
                "statements": ["Phrase 1"],
                "contradictions": []
            }
        ]

        # Act
        response = AnalysisResponse(categories=categories)

        # Assert
        assert response is not None
        assert len(response.categories) == 1

    def test_analysis_response_with_contradictions(self):
        """
        Test response with detected contradictions.
        """
        # Arrange
        categories = [
            {
                "category_name": "support",
                "statements": ["Phrase 1", "Phrase 2"],
                "contradictions": [
                    {
                        "statements": ["Phrase 1", "Phrase 2"],
                        "severity": "حاد",
                        "comment": "Test contradiction"
                    }
                ]
            }
        ]

        # Act
        response = AnalysisResponse(categories=categories)

        # Assert
        assert len(response.categories) == 1
        assert len(response.categories[0].contradictions) == 1

    def test_analysis_response_with_multiple_classifications(self, sample_sentences):
        """
        Test response with multiple classifications.
        """
        # Arrange
        categories = [
            {
                "category_name": "support",
                "statements": sample_sentences,
                "contradictions": []
            }
        ]

        # Act
        response = AnalysisResponse(categories=categories)

        # Assert
        assert len(response.categories) == 1
        assert len(response.categories[0].statements) == len(sample_sentences)

    def test_analysis_response_empty_contradictions(self, sample_sentences):
        """
        Test response with no contradictions.
        """
        # Arrange
        categories = [
            {
                "category_name": "support",
                "statements": sample_sentences,
                "contradictions": []
            }
        ]

        # Act
        response = AnalysisResponse(categories=categories)

        # Assert
        assert len(response.categories[0].contradictions) == 0

    def test_analysis_response_serialization(self):
        """
        Test serialization of the response.
        """
        # Arrange
        categories = [
            {
                "category_name": "support",
                "statements": ["Phrase 1"],
                "contradictions": []
            }
        ]
        response = AnalysisResponse(categories=categories)

        # Act
        if hasattr(response, 'model_dump'):
            data = response.model_dump()
            assert "categories" in data
