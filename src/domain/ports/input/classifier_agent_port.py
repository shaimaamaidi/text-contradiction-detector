"""
Module: classifier_agent_port
Description:
    This module defines the abstract interface for a classifier agent.
    Any concrete implementation of a classifier agent must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import List

from src.domain.models.classification_result import ClassificationResult


class ClassifierAgentPort(ABC):
    """
    Abstract interface for a classifier agent.

    Defines the methods that the domain layer can call on any classifier agent.
    """

    @abstractmethod
    def classify_sentences(self, sentences: List[str]) -> ClassificationResult:
        """
        Classifies a list of sentences and returns a ClassificationResult object.

        Args:
            sentences (List[str]): A list of sentences to classify.

        Returns:
            ClassificationResult: The classification results for the given sentences.
        """
        pass
