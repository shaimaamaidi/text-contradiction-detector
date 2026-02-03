"""
Module: classification_llm_response
Description:
    Defines the Pydantic models representing the LLM classification response.
    Categories contain 1-based indices of sentences returned by the LLM.
"""

from pydantic import BaseModel, Field
from typing import List


class CategoryLLM(BaseModel):
    """
    Represents a category returned by the LLM classification.

    Attributes:
        name (str): Name of the category. Defaults to "Unnamed".
        phrases (List[int]): List of 1-based indices of sentences belonging to this category.
    """
    name: str = Field(default="بدون اسم")
    phrases: List[int]


class ClassificationLLMResponse(BaseModel):
    """
    Represents the full classification response returned by the LLM.

    Attributes:
        categories (List[CategoryLLM]): List of categories containing sentence indices.
    """
    categories: List[CategoryLLM]
