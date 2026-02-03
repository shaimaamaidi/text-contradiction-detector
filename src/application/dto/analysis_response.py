"""
Module: analysis_response
Description:
    DTOs for the response of a text analysis request with category-based contradictions.
"""

from typing import List
from pydantic import BaseModel


class ContradictionDTO(BaseModel):
    """
    Represents a detected contradiction between sentences.

    Attributes:
        statements (List[str]): List of sentences involved in the contradiction.
        severity (str): Severity level ("حاد" or "متوسط").
        comment (str): Explanation of the contradiction in Arabic.
    """
    statements: List[str]
    severity: str
    comment: str


class CategoryContradictionDTO(BaseModel):
    """
    Represents contradictions detected within a specific category.

    Attributes:
        category_name (str): Name of the category.
        statements (List[str]): All sentences in this category.
        contradictions (List[ContradictionDTO]): List of contradictions within this category.
    """
    category_name: str
    statements: List[str]
    contradictions: List[ContradictionDTO]


class AnalysisResponse(BaseModel):
    """
    Response DTO for text analysis.

    Attributes:
        categories (List[CategoryContradictionDTO]): List of categories with their contradictions.
    """
    categories: List[CategoryContradictionDTO]
