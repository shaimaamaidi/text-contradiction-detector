"""
Module: text_analysis_service
Description:
    This module defines the TextAnalysisService, a domain service responsible for
    orchestrating the classification of sentences and the detection of logical
    contradictions between them.
"""

from typing import List

from src.domain.models.contradiction_result import AnalysisContradictionResult
from src.domain.ports.input.classifier_agent_port import ClassifierAgentPort
from src.domain.ports.input.detector_agent_port import DetectorAgentPort


class TextAnalysisService:
    """
    Domain service that orchestrates sentence classification and contradiction detection.

    This service uses a classifier agent to categorize sentences and a detector agent
    to identify contradictions among the classified sentences.
    """

    def __init__(self, classifier_agent: ClassifierAgentPort, detector_agent: DetectorAgentPort):
        """
        Initializes the TextAnalysisService with the required agents.

        Args:
            classifier_agent (ClassifierAgentPort): Agent responsible for sentence classification.
            detector_agent (DetectorAgentPort): Agent responsible for contradiction detection.
        """
        self.classifier_agent = classifier_agent
        self.detector_agent = detector_agent

    def analyze_text(self, sentences: List[str]) -> AnalysisContradictionResult:
        """
        Analyzes a list of sentences by performing classification and contradiction detection.

        The analysis is performed in two steps:
            1. Classification: Sentences are categorized by the classifier agent.
            2. Contradiction Detection: Contradictions are identified among the classified sentences.

        Args:
            sentences (List[str]): List of sentences to analyze.

        Returns:
            AnalysisContradictionResult: Object containing classification results and
                                         a list of detected contradictions.
        """
        # Classification
        classification_result = self.classifier_agent.classify_sentences(sentences)
        # Contradiction detection
        contradictions_result = self.detector_agent.detect_contradiction(classification_result)

        return contradictions_result
