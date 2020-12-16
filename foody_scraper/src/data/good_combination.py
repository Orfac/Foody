import dataclasses
from dataclasses import dataclass
from typing import List

from foody_scraper.src.data.ingredient import Ingredient


@dataclass
class GoodCombination:
    id: str
    ingredients: List[Ingredient]
    support: float
    confidence: float
    lift: float

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def get_unique_id(good_combinations_dict):
        return str(good_combinations_dict['ingredients'][0]['_id']) + str(good_combinations_dict['ingredients'][1]['_id'])
