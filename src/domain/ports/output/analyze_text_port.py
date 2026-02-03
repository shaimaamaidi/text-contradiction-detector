"""
Module: analyze_text_port
Description:
    This module defines the output port for the AnalyzeTextUseCase.
    It allows transmitting the analysis results to the interface layer (API, CLI, UI).
"""

from abc import ABC, abstractmethod

from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse


class AnalyzeTextPort(ABC):
    """
    Output port for the AnalyzeTextUseCase.
    Defines the abstract method to execute text analysis and return results.
    """

    @abstractmethod
    def execute(self, request: AnalysisRequest) -> AnalysisResponse:
        """
        Executes the text analysis use case.

        Args:
            request (AnalysisRequest): The request containing sentences to analyze.

        Returns:
            AnalysisResponse: The response containing detected contradictions.
        """
        pass
