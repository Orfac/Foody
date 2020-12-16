from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

from foody_scraper.src.data.ingredient import Ingredient


class IngredientDao:
    def __init__(self):
        self.client = MongoClient()
        self.db: Database = self.client.foody
        self.ingredients: Collection = self.db.ingredients

    def save(self, ingredient: Ingredient):
        self.ingredients.insert_one(ingredient.to_dict())

    def update_probability_measures(self, ingredient: Ingredient, new_probability_measure: str):
        probability_measures = self.find_by_id(ingredient.id)['probability_measures']

        probability_measures.append(new_probability_measure)
        self.ingredients.update_one(
            {'id': ingredient.id},
            {'$set': {'probability_measures': list(set(probability_measures))}})

    def find_by_id(self, ingredient_id: int) -> Ingredient:
        return self.ingredients.find_one({"id": ingredient_id})

    def find_by_name(self, name: str) -> Ingredient:
        return self.ingredients.find_one({"name": name})

    def drop(self):
        self.db.ingredients.drop()
