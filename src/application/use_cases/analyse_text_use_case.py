"""
Module: analyze_text_use_case
Description:
    Use case for analyzing a set of sentences:
        - Classify sentences via the classifier agent
        - Detect contradictions via the detector agent
"""

from typing import List
from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse, ContradictionDTO
from src.domain.ports.output.analyze_text_port import AnalyzeTextPort
from src.domain.services.text_analysis_service import TextAnalysisService
from src.domain.models.contradiction_result import ContradictionResult


class AnalyzeTextUseCase(AnalyzeTextPort):
    """
    Use case for analyzing a set of sentences.
    Orchestrates classification and contradiction detection.
    """

    def __init__(self, text_analysis_service: TextAnalysisService):
        """
        Initializes the use case with the domain service.

        Args:
            text_analysis_service (TextAnalysisService): Domain service for text analysis.
        """
        self.service = text_analysis_service

    def execute(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Executes the use case: classify sentences and detect contradictions.

        Args:
            request (AnalysisRequest): Sentences to be analyzed.

        Returns:
            dict: AnalysisResponse serialized as a dictionary.
        """
        if not request.sentences:
            return AnalysisResponse.model_construct(contradictions=[]).model_dump(by_alias=True)

        #  Call the domain service
        contradictions_result: List[ContradictionResult] = self.service.analyze_text(request.sentences)

        # Map domain results to DTOs
        contradictions_dto: List[ContradictionDTO] = []
        for cr in contradictions_result:
            for c in cr.contradictions:
                contradictions_dto.append(
                    ContradictionDTO.model_construct(
                        statements=c.statements,
                        severity=c.severity,
                        comment=c.comment
                    )
                )

        response_dto = AnalysisResponse.model_construct(contradictions=contradictions_dto)
        # Return as a dictionary ready for JSON serialization
        return response_dto.model_dump(by_alias=True)
