from abc import ABC, abstractmethod

from src.application.dto.analysis_request import AnalysisRequest
from src.application.dto.analysis_response import AnalysisResponse

class AnalyzeTextPort(ABC):
    """
    Port de sortie pour le use case AnalyzeTextUseCase.
    Permet de transmettre le résultat vers l'interface (API, CLI, UI).
    """

    @abstractmethod
    def execute(self, request: AnalysisRequest) -> AnalysisResponse:
        pass
