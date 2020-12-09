import dataclasses
from dataclasses import dataclass
from typing import Optional, List

from foody_scraper.src.data.good_combination import GoodCombination
from foody_scraper.src.data.ingredient import Ingredient
from foody_scraper.src.data.nutrition import Nutrition


@dataclass
class Recipe:
    link: str
    image_link: str
    title: Optional[str]
    time: Optional[str]
    n_persons: Optional[int]
    ingredients: List[Ingredient]
    good_combinations: List[GoodCombination]
    tags: List[str]
    nutritions: List[Nutrition]
    recipe_steps: List[str]

    def to_dict(self):
        return dataclasses.asdict(self)
