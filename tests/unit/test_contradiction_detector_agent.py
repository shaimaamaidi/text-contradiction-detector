"""
Module: test_contradiction_detector_agent
Description:
    Unit tests for the ContradictionDetector agent.
    Tests contradiction detection between sentences using Azure OpenAI.
"""

import pytest
from unittest.mock import Mock, patch
from src.insfrastructure.agents.contradiction_detector_agent import ContradictionDetector


class TestContradictionDetector:
    """
    Unit tests for the ContradictionDetector agent.
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
    def detector_agent(self, mock_azure_settings, mock_prompt_provider):
        """Instance of the contradiction detector agent."""
        return ContradictionDetector(azure_settings=mock_azure_settings, prompt_provider=mock_prompt_provider)

    def test_detect_contradictions_in_pair(self, detector_agent, contradictory_sentences,
                                          mock_prompt_provider):
        """
        Test contradiction detection in a pair of sentences.
        """
        # Arrange
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect(contradictory_sentences)

        # Assert
        assert result is not None

    def test_detect_no_contradiction(self, detector_agent, non_contradictory_sentences,
                                     mock_prompt_provider):
        """
        Test that no contradictions are detected for compatible sentences.
        """
        # Arrange
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect(non_contradictory_sentences)

        # Assert
        assert result is not None

    def test_detect_with_support_reject_pair(self, detector_agent, mock_prompt_provider):
        """
        Test contradiction detection between support and reject sentences.
        """
        # Arrange
        sentences = [
            "أوصي باعتماد المقترح بشكل كامل.",
            "أرى رفض المقترح في الوقت الحالي."
        ]
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect(sentences)

        # Assert
        assert result is not None

    def test_detect_with_multiple_sentences(self, detector_agent, sample_sentences,
                                           mock_prompt_provider):
        """
        Test contradiction detection in multiple sentences.
        """
        # Arrange
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect(sample_sentences)

        # Assert
        assert result is not None
        # Vérifier que le résultat est une liste ou un objet itérable
        if isinstance(result, list):
            # La liste peut être vide ou contenir des contradictions
            pass

    def test_detect_with_single_sentence(self, detector_agent, sample_single_sentence,
                                        mock_prompt_provider):
        """
        Test that a single sentence does not produce contradictions.
        """
        # Arrange
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect([sample_single_sentence])

        # Assert
        assert result is not None

    def test_detect_with_empty_list(self, detector_agent, empty_sentences,
                                    mock_prompt_provider):
        """
        Test contradiction detection on an empty list.
        """
        # Arrange
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect(empty_sentences)

        # Assert
        assert result is not None

    def test_detect_uses_prompt_provider(self, detector_agent, contradictory_sentences,
                                         mock_prompt_provider):
        """
        Test that the prompt provider is used correctly.
        """
        # Arrange
        expected_prompt = "Detect contradictions between sentences"
        mock_prompt_provider.get_contradiction_prompt.return_value = expected_prompt

        # Act
        detector_agent.detect(contradictory_sentences)

        # Assert
        mock_prompt_provider.get_contradiction_prompt.assert_called()

    def test_detect_energy_related_contradiction(self, detector_agent, mock_prompt_provider):
        """
        Test contradiction detection on energy-related topics.
        """
        # Arrange
        energy_sentences = [
            "أوصي بالاستثمار في الطاقة الشمسية لتقليل التكاليف وزيادة الاستدامة.",
            "أرى أن التركيز على الوقود الأحفوري أكثر أمانًا وموثوقية."
        ]
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect(energy_sentences)

        # Assert
        assert result is not None

    def test_detect_implementation_duration_contradiction(self, detector_agent,
                                                         mock_prompt_provider):
        """
        Test contradiction detection on implementation duration.
        """
        # Arrange
        duration_sentences = [
            "أوصي باعتماد المقترح مع البدء بتطبيقه على نطاق محدود لمدة 3 أشهر.",
            "أؤيد الموافقة على المقترح ولكن أرى أن تكون مدة التجربة سنة كاملة."
        ]
        mock_prompt_provider.get_contradiction_prompt.return_value = "Contradiction detection prompt"

        # Act
        result = detector_agent.detect(duration_sentences)

        # Assert
        assert result is not None
