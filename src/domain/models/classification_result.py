from typing import List
from dataclasses import dataclass

@dataclass
class Category:
    name: str
    phrases: List[str]

@dataclass
class ClassificationResult:
    categories: List[Category]