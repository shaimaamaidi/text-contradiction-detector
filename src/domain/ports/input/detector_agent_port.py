from abc import ABC, abstractmethod
from typing import List, Dict

from src.domain.models.classification_result import ClassificationResult
from src.domain.models.contradiction_result import ContradictionResult


class DetectorAgentPort(ABC):
    """
    Interface abstraite pour tout agent.
    Définit les méthodes que le domaine peut appeler.
    """


    @abstractmethod
    def detect_contradiction(
        self, classification_result: ClassificationResult
    ) -> List[ContradictionResult]:
        """
        Analyse les phrases par catégorie et retourne les contradictions détectées.
        """
        pass
