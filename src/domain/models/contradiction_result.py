"""
Module: contradiction_result
Description:
    Domain models representing contradictions detected in sentences.
    Each Contradiction contains the sentences involved, a severity level, and an explanatory comment.
"""

from dataclasses import dataclass
from typing import List


@dataclass
class Contradiction:
    """
    Represents a single contradiction between sentences.

    Attributes:
        statements (List[str]): List of sentences involved in the contradiction.
        severity (str): Severity level of the contradiction ("حاد" ou "متوسط").
        comment (str): Explanation or comment about the contradiction.
    """
    statements: List[str]
    severity: str
    comment: str


@dataclass
class ContradictionResult:
    """
    Contains a list of contradictions detected in a set of sentences.

    Attributes:
        contradictions (List[Contradiction]): List of detected contradictions.
    """
    contradictions: List[Contradiction]
