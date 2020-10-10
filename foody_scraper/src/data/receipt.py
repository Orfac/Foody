from dataclasses import dataclass
from typing import Optional, List

from foody_scraper.src.data.ingredient import Ingredient


@dataclass
class Receipt:
    title: Optional[str]
    time: Optional[str]
    n_persons: Optional[int]
    ingredients: List[Ingredient]