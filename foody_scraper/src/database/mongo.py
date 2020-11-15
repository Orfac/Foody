import dataclasses

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from foody_scraper.src.data.recipe import Recipe


class Mongo:
    def __init__(self):
        self.client = MongoClient()
        self.db: Database = self.client.foody
        self.recipes: Collection = self.db.recipes

    def save(self, recipe: Recipe):
        self.recipes.insert_one(recipe.to_dict())

    def save_all(self, recipes: [Recipe]):
        self.recipes.insert_many(
            [recipe.to_dict() for recipe in recipes]
        )

    def drop(self):
        self.db.recipes.drop()

    def find_all(self):
        return list(self.recipes.find({}))

    def find_by_title(self, title):
        return self.recipes.find_one(
            {"title": title}
        )
