from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from foody_scraper.src.data.good_combination import GoodCombination
from foody_scraper.src.data.recipe import Recipe


class Mongo:
    def __init__(self):
        self.client = MongoClient()
        self.db: Database = self.client.foody
        self.recipes: Collection = self.db.recipes

    def save(self, recipe: Recipe):
        self.recipes.insert_one(recipe.to_dict())

    def set_good_combinations_for_recipe(self, recipe: Recipe, new_good_combination: GoodCombination):
        good_combinations = self.find_by_title(recipe['title'])['good_combinations']
        good_combination_ids = [good_combination['id'] for good_combination in good_combinations]

        if new_good_combination.id not in good_combination_ids:
            good_combinations.append(new_good_combination.to_dict())
            self.recipes.update_one(
                {'title': recipe['title']},
                {'$set': {'good_combinations': good_combinations}}
            )

    def save_all(self, recipes: [Recipe]):
        self.recipes.insert_many(
            [recipe.to_dict() for recipe in recipes]
        )

    def drop(self):
        self.db.recipes.drop()

    def find_all(self) -> List[Recipe]:
        return list(self.recipes.find({}))

    def find_by_title(self, title):
        return self.recipes.find_one({"title": title})

    def find_by_link(self, receipt_link) -> Recipe:
        return self.recipes.find_one({"link": receipt_link})
