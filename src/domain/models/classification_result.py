"""
Module: classification_models
Description:
    This module defines data structures for text classification results.
    It includes:
        - Category: a semantic category with associated phrases.
        - ClassificationResult: result of a classification process containing multiple categories.
"""

from typing import List
from dataclasses import dataclass


@dataclass
class Category:
    """
    Represents a semantic category with associated phrases.

    Attributes:
        name (str): The name of the category.
        phrases (List[str]): List of phrases belonging to this category.
    """
    name: str
    phrases: List[str]

@dataclass
class ClassificationResult:
    """
    Represents the result of a classification process.

    Attributes:
        categories (List[Category]): List of categorized phrases.
    """
    categories: List[Category]
