import dataclasses
from dataclasses import dataclass
from typing import Optional, List

from foody_scraper.src.data.ingredient import Ingredient
from foody_scraper.src.data.nutrition import Nutrition


@dataclass
class Recipe:
    receipt_link: str
    title: Optional[str]
    time: Optional[str]
    n_persons: Optional[int]
    ingredients: List[Ingredient]
    tags: List[str]
    nutritions: List[Nutrition]
    recipe_steps: List[str]

    def to_dict(self):
        return dataclasses.asdict(self)
