from typing import List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from foody_scraper.src.data.ingredient import Ingredient
from foody_scraper.src.data.recipe import Recipe


class Mongo:
    def __init__(self):
        self.client = MongoClient()
        self.db: Database = self.client.foody
        self.ingredients: Collection = self.db.ingredients
        self.recipes: Collection = self.db.recipes

    def save(self, recipe: Recipe):
        self.recipes.insert_one(recipe.to_dict())

    def update_recipe(self, recipe: Recipe):
        self.recipes.update_one(recipe.to_dict())

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

    def save_ingredient(self, ingredient: Ingredient):
        self.ingredients.insert_one(ingredient.to_dict())

    def find_ingredient_by_id(self, ingredient_id: int) -> Ingredient:
        return self.ingredients.find_one({"id": ingredient_id})

    def find_ingredient_by_name(self, name: str) -> Ingredient:
        return self.ingredients.find_one({"name": name})
