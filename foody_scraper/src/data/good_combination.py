import dataclasses
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

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def generate_id(ingredients: List[Ingredient]):
        concatenated_titles = ' '.join([
            ingredient.name if isinstance(ingredient, Ingredient) else ingredient['name'] for ingredient in ingredients
        ])
        return hash(concatenated_titles)
