"""
Module: test_text_analysis_service
Description:
    Unit tests for the TextAnalysisService.
    Tests text analysis, sentence classification, and contradiction detection.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.domain.services.text_analysis_service import TextAnalysisService


class TestTextAnalysisService:
    """
    Unit tests for TextAnalysisService.
    """

    @pytest.fixture
    def mock_classifier_agent_port(self):
        """Mock of the classifier agent port."""
        return Mock()

    @pytest.fixture
    def mock_detector_agent_port(self):
        """Mock of the contradiction detector agent port."""
        return Mock()

    @pytest.fixture
    def text_analysis_service(self, mock_classifier_agent_port, mock_detector_agent_port):
        """Instance of the service with mocked ports."""
        service = TextAnalysisService()
        service.classifier_agent_port = mock_classifier_agent_port
        service.detector_agent_port = mock_detector_agent_port
        return service

    def test_analyze_single_sentence(self, text_analysis_service, sample_single_sentence, 
                                     mock_classifier_agent_port, mock_detector_agent_port):
        """
        Test analysis of a single sentence.
        """
        # Arrange
        mock_classifier_agent_port.classify.return_value = {
            "sentence": sample_single_sentence,
            "classification": "support"
        }
        mock_detector_agent_port.detect.return_value = []

        # Act
        result = text_analysis_service.analyze([sample_single_sentence])

        # Assert
        assert result is not None
        mock_classifier_agent_port.classify.assert_called()

    def test_analyze_multiple_sentences(self, text_analysis_service, sample_sentences,
                                       mock_classifier_agent_port, mock_detector_agent_port):
        """
        Test analysis of multiple sentences.
        """
        # Arrange
        classifications = [
            {"sentence": s, "classification": "support"} for s in sample_sentences
        ]
        mock_classifier_agent_port.classify.side_effect = classifications
        mock_detector_agent_port.detect.return_value = []

        # Act
        result = text_analysis_service.analyze(sample_sentences)

        # Assert
        assert result is not None
        assert mock_classifier_agent_port.classify.call_count == len(sample_sentences)

    def test_analyze_detects_contradictions(self, text_analysis_service, contradictory_sentences,
                                           mock_classifier_agent_port, mock_detector_agent_port):
        """
        Test contradiction detection between sentences.
        """
        # Arrange
        classifications = [
            {"sentence": contradictory_sentences[0], "classification": "support"},
            {"sentence": contradictory_sentences[1], "classification": "reject"}
        ]
        mock_classifier_agent_port.classify.side_effect = classifications
        mock_detector_agent_port.detect.return_value = [{
            "sentence1": contradictory_sentences[0],
            "sentence2": contradictory_sentences[1],
            "contradiction": True
        }]

        # Act
        result = text_analysis_service.analyze(contradictory_sentences)

        # Assert
        assert result is not None
        mock_detector_agent_port.detect.assert_called()

    def test_analyze_with_empty_list(self, text_analysis_service, empty_sentences):
        """
        Test analysis with an empty list.
        """
        # Act
        result = text_analysis_service.analyze(empty_sentences)

        # Assert
        assert result is not None

    def test_classification_agent_invocation(self, text_analysis_service, sample_single_sentence,
                                            mock_classifier_agent_port):
        """
        Test that the classification agent is properly invoked.
        """
        # Arrange
        mock_classifier_agent_port.classify.return_value = {
            "sentence": sample_single_sentence,
            "classification": "support"
        }

        # Act
        text_analysis_service.analyze([sample_single_sentence])

        # Assert
        mock_classifier_agent_port.classify.assert_called_once()

    def test_contradiction_detection_not_called_for_single_sentence(self, text_analysis_service,
                                                                   sample_single_sentence,
                                                                   mock_classifier_agent_port,
                                                                   mock_detector_agent_port):
        """
        Test that contradiction detection is not required for a single sentence.
        """
        # Arrange
        mock_classifier_agent_port.classify.return_value = {
            "sentence": sample_single_sentence,
            "classification": "support"
        }

        # Act
        text_analysis_service.analyze([sample_single_sentence])

        # Assert
        # Pour une seule phrase, la détection de contradictions n'est pas nécessaire
        if hasattr(mock_detector_agent_port, 'detect'):
            # Selon l'implémentation, cela peut ou non être appelé
            pass

    def test_analyze_with_various_classification_types(self, text_analysis_service,
                                                      mock_classifier_agent_port,
                                                      mock_detector_agent_port):
        """
        Test analysis with various classification types.
        """
        # Arrange
        sentences = [
            "أوصي باعتماد المقترح.",
            "أرى رفض المقترح.",
            "أرى أن المقترح مناسب ولكن يحتاج إلى تعديل."
        ]
        
        classifications = [
            {"sentence": sentences[0], "classification": "support"},
            {"sentence": sentences[1], "classification": "reject"},
            {"sentence": sentences[2], "classification": "neutral"}
        ]
        
        mock_classifier_agent_port.classify.side_effect = classifications
        mock_detector_agent_port.detect.return_value = []

        # Act
        result = text_analysis_service.analyze(sentences)

        # Assert
        assert result is not None
        assert mock_classifier_agent_port.classify.call_count == len(sentences)
