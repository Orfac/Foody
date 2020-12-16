import dataclasses
from dataclasses import dataclass
from typing import List


@dataclass
class Ingredient:
    id: int
    name: str
    probability_measures: List[str]

    def to_dict(self):
        return dataclasses.asdict(self)

    @staticmethod
    def convert_dict_to_ingredient(ingredient_dict):
        return Ingredient(id=ingredient_dict['id'],
                          name=ingredient_dict['name'],
                          probability_measures=ingredient_dict['probability_measures'])