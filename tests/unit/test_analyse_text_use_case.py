"""
Module: test_analyse_text_use_case
Description:
    Unit tests for the AnalyzeTextUseCase.
    Tests the orchestration of sentence classification and contradiction detection.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from src.application.use_cases.analyse_text_use_case import AnalyzeTextUseCase
from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse


class TestAnalyzeTextUseCase:
    """
    Unit tests for the AnalyzeTextUseCase.
    """

    @pytest.fixture
    def mock_text_analysis_service(self):
        """Mock of the text analysis service."""
        return Mock()

    @pytest.fixture
    def analyse_use_case(self, mock_text_analysis_service):
        """Instance of the use case with mocked service."""
        return AnalyzeTextUseCase(text_analysis_service=mock_text_analysis_service)

    def test_execute_with_valid_sentences(self, analyse_use_case, sample_sentences, mock_text_analysis_service):
        """
        Test execution with valid sentences.
        """
        # Arrange
        request = AnalysisRequest(sentences=sample_sentences)
        expected_response = AnalysisResponse(
            classifications=[{"sentence": s, "classification": "support"} for s in sample_sentences],
            contradictions=[]
        )
        mock_text_analysis_service.analyze.return_value = expected_response

        # Act
        result = analyse_use_case.execute(request)

        # Assert
        assert result is not None
        mock_text_analysis_service.analyze.assert_called_once_with(sample_sentences)

    def test_execute_with_empty_sentences(self, analyse_use_case, mock_text_analysis_service):
        """
        Test execution with an empty list of sentences.
        """
        # Arrange
        request = AnalysisRequest(sentences=[])
        mock_text_analysis_service.analyze.return_value = AnalysisResponse(
            classifications=[],
            contradictions=[]
        )

        # Act
        result = analyse_use_case.execute(request)

        # Assert
        assert result is not None
        assert result.classifications == []
        assert result.contradictions == []

    def test_execute_with_single_sentence(self, analyse_use_case, sample_single_sentence, mock_text_analysis_service):
        """
        Test execution with a single sentence.
        """
        # Arrange
        request = AnalysisRequest(sentences=[sample_single_sentence])
        expected_response = AnalysisResponse(
            classifications=[{"sentence": sample_single_sentence, "classification": "support"}],
            contradictions=[]
        )
        mock_text_analysis_service.analyze.return_value = expected_response

        # Act
        result = analyse_use_case.execute(request)

        # Assert
        assert result is not None
        assert len(result.classifications) == 1

    def test_execute_detects_contradictions(self, analyse_use_case, contradictory_sentences, mock_text_analysis_service):
        """
        Test that the use case detects contradictions.
        """
        # Arrange
        request = AnalysisRequest(sentences=contradictory_sentences)
        expected_response = AnalysisResponse(
            classifications=[
                {"sentence": contradictory_sentences[0], "classification": "support"},
                {"sentence": contradictory_sentences[1], "classification": "reject"}
            ],
            contradictions=[{
                "sentence1": contradictory_sentences[0],
                "sentence2": contradictory_sentences[1],
                "contradiction_detected": True
            }]
        )
        mock_text_analysis_service.analyze.return_value = expected_response

        # Act
        result = analyse_use_case.execute(request)

        # Assert
        assert result is not None
        assert len(result.contradictions) > 0

    def test_execute_service_exception_handling(self, analyse_use_case, sample_sentences, mock_text_analysis_service):
        """
        Test service exception handling.
        """
        # Arrange
        request = AnalysisRequest(sentences=sample_sentences)
        mock_text_analysis_service.analyze.side_effect = Exception("Service error")

        # Act & Assert
        with pytest.raises(Exception):
            analyse_use_case.execute(request)

    def test_execute_with_non_contradictory_sentences(self, analyse_use_case, non_contradictory_sentences, mock_text_analysis_service):
        """
        Test execution with non-contradictory sentences.
        """
        # Arrange
        request = AnalysisRequest(sentences=non_contradictory_sentences)
        expected_response = AnalysisResponse(
            classifications=[
                {"sentence": non_contradictory_sentences[0], "classification": "support"},
                {"sentence": non_contradictory_sentences[1], "classification": "support"}
            ],
            contradictions=[]
        )
        mock_text_analysis_service.analyze.return_value = expected_response

        # Act
        result = analyse_use_case.execute(request)

        # Assert
        assert result is not None
        assert len(result.contradictions) == 0
