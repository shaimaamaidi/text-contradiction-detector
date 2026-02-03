from abc import ABC, abstractmethod
from typing import List

from src.domain.models.classification_result import ClassificationResult


class ClassifierAgentPort(ABC):
    """
    Interface abstraite pour tout agent.
    Définit les méthodes que le domaine peut appeler.
    """

    @abstractmethod
    def classify_sentences(self, sentences: List[str]) -> ClassificationResult:
        """
        Classe un ensemble de phrases et retourne un objet ClassificationResponse
        """
        pass

