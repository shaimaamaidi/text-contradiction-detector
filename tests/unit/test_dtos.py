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
        classifications = [
            {"sentence": "Phrase 1", "classification": "support"}
        ]
        contradictions = []

        # Act
        response = AnalysisResponse(
            classifications=classifications,
            contradictions=contradictions
        )

        # Assert
        assert response is not None
        assert response.classifications == classifications
        assert response.contradictions == contradictions

    def test_analysis_response_with_contradictions(self):
        """
        Test response with detected contradictions.
        """
        # Arrange
        classifications = [
            {"sentence": "Phrase 1", "classification": "support"},
            {"sentence": "Phrase 2", "classification": "reject"}
        ]
        contradictions = [
            {
                "sentence1": "Phrase 1",
                "sentence2": "Phrase 2",
                "contradiction": True
            }
        ]

        # Act
        response = AnalysisResponse(
            classifications=classifications,
            contradictions=contradictions
        )

        # Assert
        assert len(response.contradictions) == 1
        assert response.contradictions[0]["contradiction"] is True

    def test_analysis_response_with_multiple_classifications(self, sample_sentences):
        """
        Test response with multiple classifications.
        """
        # Arrange
        classifications = [
            {"sentence": s, "classification": "support"} for s in sample_sentences
        ]

        # Act
        response = AnalysisResponse(
            classifications=classifications,
            contradictions=[]
        )

        # Assert
        assert len(response.classifications) == len(sample_sentences)

    def test_analysis_response_empty_contradictions(self, sample_sentences):
        """
        Test response with no contradictions.
        """
        # Arrange
        classifications = [
            {"sentence": s, "classification": "support"} for s in sample_sentences
        ]

        # Act
        response = AnalysisResponse(
            classifications=classifications,
            contradictions=[]
        )

        # Assert
        assert len(response.contradictions) == 0

    def test_analysis_response_serialization(self):
        """
        Test serialization of the response.
        """
        # Arrange
        classifications = [
            {"sentence": "Phrase 1", "classification": "support"}
        ]
        response = AnalysisResponse(
            classifications=classifications,
            contradictions=[]
        )

        # Act
        if hasattr(response, 'dict'):
            data = response.dict()
            assert "classifications" in data
            assert "contradictions" in data
