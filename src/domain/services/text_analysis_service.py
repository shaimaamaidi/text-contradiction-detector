from typing import List

from src.domain.models.contradiction_result import ContradictionResult
from src.domain.ports.input.classifier_agent_port import ClassifierAgentPort
from src.domain.ports.input.detector_agent_port import DetectorAgentPort


class TextAnalysisService:
    """
    Service du domaine qui orchestre la classification et la détection
    des contradictions.
    """

    def __init__(self, classifier_agent: ClassifierAgentPort, detector_agent: DetectorAgentPort):

        self.classifier_agent = classifier_agent
        self.detector_agent = detector_agent

    def analyze_text(self, sentences: List[str]) -> List[ContradictionResult]:
        """
        Analyse un ensemble de phrases :
        1. Classification
        2. Détection des contradictions

        Returns:
            classification: ClassificationResponse
            contradictions: List[ContradictionResponse]
        """
        # Étape 1 : Classification
        classification_result = self.classifier_agent.classify_sentences(sentences)
        # Étape 2 : Détection de contradictions
        contradictions_result = self.detector_agent.detect_contradiction(classification_result)

        return contradictions_result
