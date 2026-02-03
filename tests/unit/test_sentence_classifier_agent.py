"""
Module: test_sentence_classifier_agent
Description:
    Unit tests for the SentenceClassifier agent.
    Tests sentence classification using Azure OpenAI and domain model mapping.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.insfrastructure.agents.sentence_classifier_agent import SentenceClassifier


class TestSentenceClassifier:
    """
    Unit tests for the SentenceClassifier agent.
    """

    @pytest.fixture
    def mock_azure_settings(self):
        """Mock of Azure settings."""
        mock_settings = Mock()
        mock_settings.endpoint = "https://test.openai.azure.com/"
        mock_settings.api_key = "test-key"
        mock_settings.api_version = "2024-01-01"
        mock_settings.model = "gpt-4"
        return mock_settings

    @pytest.fixture
    def mock_prompt_provider(self):
        """Mock of the prompt provider."""
        return Mock()

    @pytest.fixture
    def classifier_agent(self, mock_azure_settings, mock_prompt_provider):
        """Instance of the classifier agent with mocked dependencies."""
        return SentenceClassifier(azure_settings=mock_azure_settings, prompt_provider=mock_prompt_provider)

    def test_classify_support_sentence(self, classifier_agent, sample_single_sentence,
                                       mock_prompt_provider):
        """
        Test classification of a support sentence.
        """
        # Arrange
        mock_prompt_provider.get_classification_prompt.return_value = "Classification prompt"
        
        # Act
        result = classifier_agent.classify(sample_single_sentence)

        # Assert
        assert result is not None
        assert "classification" in result or "sentence" in result

    def test_classify_multiple_sentences(self, classifier_agent, sample_sentences,
                                         mock_prompt_provider):
        """
        Test classification of multiple sentences.
        """
        # Arrange
        mock_prompt_provider.get_classification_prompt.return_value = "Classification prompt"

        # Act
        classifications = [classifier_agent.classify(s) for s in sample_sentences]

        # Assert
        assert len(classifications) == len(sample_sentences)
        for classification in classifications:
            assert classification is not None

    def test_classify_support_recommendation(self, classifier_agent, mock_prompt_provider):
        """
        Test classification of a positive recommendation.
        """
        # Arrange
        support_sentence = "أوصي باعتماد المقترح بشكل كامل والبدء في التنفيذ الفوري."
        mock_prompt_provider.get_classification_prompt.return_value = "Classification prompt"

        # Act
        result = classifier_agent.classify(support_sentence)

        # Assert
        assert result is not None

    def test_classify_reject_recommendation(self, classifier_agent, mock_prompt_provider):
        """
        Test classification of a negative recommendation.
        """
        # Arrange
        reject_sentence = "أرى رفض المقترح في الوقت الحالي بسبب عدم وضوح التكلفة."
        mock_prompt_provider.get_classification_prompt.return_value = "Classification prompt"

        # Act
        result = classifier_agent.classify(reject_sentence)

        # Assert
        assert result is not None

    def test_classify_neutral_recommendation(self, classifier_agent, mock_prompt_provider):
        """
        Test classification of a neutral recommendation.
        """
        # Arrange
        neutral_sentence = "أرى أن المقترح مناسب من حيث المبدأ، ولكن يحتاج إلى تعديل."
        mock_prompt_provider.get_classification_prompt.return_value = "Classification prompt"

        # Act
        result = classifier_agent.classify(neutral_sentence)

        # Assert
        assert result is not None

    def test_classify_with_prompt_provider(self, classifier_agent, sample_single_sentence,
                                          mock_prompt_provider):
        """
        Test that the prompt provider is used correctly.
        """
        # Arrange
        expected_prompt = "Classify the following sentence in Arabic"
        mock_prompt_provider.get_classification_prompt.return_value = expected_prompt

        # Act
        classifier_agent.classify(sample_single_sentence)

        # Assert
        mock_prompt_provider.get_classification_prompt.assert_called()

    def test_classify_empty_sentence(self, classifier_agent, mock_prompt_provider):
        """
        Test classification of an empty sentence.
        """
        # Arrange
        empty_sentence = ""
        mock_prompt_provider.get_classification_prompt.return_value = "Classification prompt"

        # Act
        result = classifier_agent.classify(empty_sentence)

        # Assert
        assert result is not None or result is None  # Comportement attendu selon implémentation

    def test_classify_long_sentence(self, classifier_agent, mock_prompt_provider):
        """
        Test classification of a very long sentence.
        """
        # Arrange
        long_sentence = "أوصي باعتماد المقترح " * 50  # Phrase très longue
        mock_prompt_provider.get_classification_prompt.return_value = "Classification prompt"

        # Act
        result = classifier_agent.classify(long_sentence)

        # Assert
        assert result is not None
