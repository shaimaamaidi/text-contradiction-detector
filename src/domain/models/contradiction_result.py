"""
Module: contradiction_result
Description:
    Domain models representing contradictions detected in sentences,
    organized per category. Each Contradiction contains the sentences involved,
    a severity level, and an explanatory comment.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Contradiction:
    """
    Represents a single contradiction between sentences.

    Attributes:
        statements (List[str]): List of sentences involved in the contradiction.
        severity (str): Severity level of the contradiction ("حاد" or "متوسط").
        comment (str): Explanation or comment about the contradiction.
    """
    statements: List[str]
    severity: str
    comment: str


@dataclass
class CategoryContradictionResult:
    """
    Represents contradictions detected within a specific category.

    Attributes:
        category_name (str): Name of the category.
        statements (List[str]): All sentences in this category.
        contradictions (List[Contradiction]): List of contradictions within this category.
    """
    category_name: str
    statements: List[str]
    contradictions: List[Contradiction]


@dataclass
class AnalysisContradictionResult:
    """
    Represents the full analysis result across all categories.

    Attributes:
        categories (List[CategoryContradictionResult]): List of categories with their contradictions.
    """
    categories: List[CategoryContradictionResult]
