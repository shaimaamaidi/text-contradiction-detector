"""
Module: contradiction_llm_response
Description:
    Defines Pydantic models representing the LLM response for detected contradictions.
    Each contradiction references sentences by 1-based indices.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List


class ContradictionLLM(BaseModel):
    """
    Represents a single contradiction detected by the LLM.

    Attributes:
        statements (List[int]): List of 1-based indices of the sentences involved in the contradiction.
        severity_level (str): Severity of the contradiction ("حاد" ou "متوسط").
        comment (str): Explanation or comment about the contradiction.
    """
    statements: List[int] = Field(alias="إفادات")
    severity_level: str = Field(alias="مستوى_التعارض")  # "حاد" ou "متوسط"
    comment: str = Field(alias="تعليق")

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )

class ContradictionLLMResponse(BaseModel):
    """
    Represents the full contradiction detection response returned by the LLM.

    Attributes:
        contradictions (List[ContradictionLLM]): List of contradictions detected.
    """
    contradictions: List[ContradictionLLM] = Field(alias="التناقضات")

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True
    )
