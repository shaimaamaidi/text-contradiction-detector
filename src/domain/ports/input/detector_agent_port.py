"""
Module: detector_agent_port
Description:
    This module defines the abstract interface for a contradiction detection agent.
    Any concrete implementation of a detector agent must implement this interface.
"""

from abc import ABC, abstractmethod

from src.domain.models.classification_result import ClassificationResult
from src.domain.models.contradiction_result import AnalysisContradictionResult


class DetectorAgentPort(ABC):
    """
    Abstract interface for a contradiction detection agent.

    Defines the methods that the domain layer can call on any detector agent.
    """

    @abstractmethod
    def detect_contradiction(
        self, classification_result: ClassificationResult
    ) -> AnalysisContradictionResult:
        """
        Analyzes classified sentences by category and returns detected contradictions.

        Args:
            classification_result (ClassificationResult): The results of sentence classification.

        Returns:
            AnalysisContradictionResult: Object containing the detected contradictions.
        """
        pass
