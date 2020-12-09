from dataclasses import dataclass
from typing import List

from foody_scraper.src.data.ingredient import Ingredient


@dataclass
class GoodCombination:
    id: int
    ingredients: List[Ingredient]
    support: float
    confidence: float
    lift: float
