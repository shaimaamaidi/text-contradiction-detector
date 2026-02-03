"""
Module: analyze_text_use_case
Description:
    Use case for analyzing a set of sentences:
        - Classify sentences via the classifier agent
        - Detect contradictions via the detector agent
"""

from typing import List
from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse, ContradictionDTO, CategoryContradictionDTO
from src.domain.models.contradiction_result import AnalysisContradictionResult
from src.domain.ports.output.analyze_text_port import AnalyzeTextPort
from src.domain.services.text_analysis_service import TextAnalysisService


class AnalyzeTextUseCase(AnalyzeTextPort):
    """
    Use case for analyzing a set of sentences.
    Orchestrates classification and contradiction detection.
    """

    def __init__(self, text_analysis_service: TextAnalysisService):
        self.service = text_analysis_service

    def execute(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Executes the use case: classify sentences and detect contradictions.

        Args:
            request (AnalysisRequest): Sentences to be analyzed.

        Returns:
            AnalysisResponse: Response DTO with categories and contradictions.
        """
        if not request.sentences:
            return AnalysisResponse.model_construct(categories=[])

        # Call the domain service
        analysis_result: AnalysisContradictionResult = self.service.analyze_text(request.sentences)

        categories_dto: List[CategoryContradictionDTO] = []

        # Map domain results to DTOs
        for category_result in analysis_result.categories:
            contradictions_dto: List[ContradictionDTO] = [
                ContradictionDTO(
                    statements=c.statements,
                    severity=c.severity,
                    comment=c.comment
                )
                for c in category_result.contradictions
            ]

            categories_dto.append(
                CategoryContradictionDTO(
                    category_name=category_result.category_name,
                    statements=category_result.statements,
                    contradictions=contradictions_dto
                )
            )

        return AnalysisResponse(categories=categories_dto)
