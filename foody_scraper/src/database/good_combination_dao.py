from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from foody_scraper.src.data.good_combination import GoodCombination
from foody_scraper.src.data.ingredient import Ingredient


class GoodCombinationDao:
    def __init__(self):
        self.client = MongoClient()
        self.db: Database = self.client.foody
        self.good_combinations: Collection = self.db.good_combinations

    def save(self, good_combination: GoodCombination):
        self.good_combinations.insert_one(good_combination.to_dict())

    def find_by_id(self, good_combination_id: str) -> Ingredient:
        return self.good_combinations.find_one({"id": good_combination_id})

    def drop(self):
        self.db.good_combinations.drop()

    def find_all(self) -> List[GoodCombination]:
        return list(self.good_combinations.find({}))
