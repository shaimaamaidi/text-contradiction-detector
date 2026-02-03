"""
Module: analysis_response
Description:
    This module defines data transfer objects (DTOs) for the response of a text analysis request.
"""

from typing import List
from pydantic import BaseModel, Field, ConfigDict


class ContradictionDTO(BaseModel):
    """
    DTO representing a detected contradiction between sentences.

    Attributes:
        statements (List[str]): List of sentences involved in the contradiction.
        severity (str): Severity level of the contradiction ("حاد" or "متوسط").
        comment (str): Explanation of the contradiction in Arabic.
    """
    statements: List[str] = Field(alias="إفادات")
    severity: str = Field(alias="مستوى_التعارض")
    comment: str = Field(alias="تعليق")

    model_config = ConfigDict(
        populate_by_name=True
    )


class AnalysisResponse(BaseModel):
    """
    DTO for the response of a text analysis request.

    Attributes:
        contradictions (List[ContradictionDTO]): List of detected contradictions.
    """
    contradictions: List[ContradictionDTO] = Field(alias="التناقضات")

    model_config = ConfigDict(
        populate_by_name=True
    )