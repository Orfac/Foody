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
