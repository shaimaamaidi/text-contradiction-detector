from typing import List
from pydantic import BaseModel

class AnalysisRequest(BaseModel):
    """
    DTO pour la requête de classification et d'analyse de texte.
    """
    sentences: List[str]
