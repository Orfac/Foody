import dataclasses
from dataclasses import dataclass


@dataclass
class Ingredient:
    id: int
    name: str

    def to_dict(self):
        return dataclasses.asdict(self)
