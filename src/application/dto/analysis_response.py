from typing import List, Dict
from pydantic import BaseModel

class ContradictionDTO(BaseModel):
    sentences: List[str]        # Numéros des phrases en contradiction
    severity: str               # "حاد" ou "متوسط"
    comment: str                # Explication en arabe

class AnalysisResponse(BaseModel):
    contradictions: List[ContradictionDTO]