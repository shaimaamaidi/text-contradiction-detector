from typing import List
from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse, ContradictionDTO
from src.domain.ports.output.analyze_text_port import AnalyzeTextPort
from src.domain.services.text_analysis_service import TextAnalysisService
from src.domain.models.contradiction_result import ContradictionResult

class AnalyzeTextUseCase(AnalyzeTextPort):
    """
    Cas d'utilisation pour analyser un ensemble de phrases :
    - Classification via classifier_agent
    - Détection des contradictions via detector_agent
    """

    def __init__(self, text_analysis_service: TextAnalysisService ):
        self.service = text_analysis_service

    def execute(self, request: AnalysisRequest) -> AnalysisResponse:
        if not request.sentences:
            return AnalysisResponse(contradictions=[])

        # Étape 1 : appeler le service du domaine
        contradictions_result: List[ContradictionResult] = self.service.analyze_text(request.sentences)
        # Étape 2 : transformer les résultats du domaine en DTO
        contradictions_dto: List[ContradictionDTO] = []
        for cr in contradictions_result:
            for c in cr.contradictions:
                contradictions_dto.append(
                    ContradictionDTO(
                        sentences=c.sentences,
                        severity=c.severity,
                        comment=c.comment
                    )
                )

        return AnalysisResponse(contradictions=contradictions_dto)
