"""
Module: analysis_request
Description:
    This module defines the data transfer object (DTO) for a text analysis request.
    It includes:
        - AnalysisRequest: DTO containing sentences to be analyzed for classification or contradiction detection.
"""

from typing import List
from pydantic import BaseModel


class AnalysisRequest(BaseModel):
    """
    DTO for a text classification and analysis request.

    Attributes:
        sentences (List[str]): A list of sentences to be analyzed.
    """
    sentences: List[str]
