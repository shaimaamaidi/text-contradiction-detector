from dataclasses import dataclass
from typing import List

@dataclass
class Contradiction:
    sentences: List[str]
    severity: str
    comment: str

@dataclass
class ContradictionResult:
    contradictions: List[Contradiction]
