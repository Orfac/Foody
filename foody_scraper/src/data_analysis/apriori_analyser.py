from typing import List

import pandas as pd
from apyori import apriori

from foody_scraper.src.data.good_combination import GoodCombination
from foody_scraper.src.data.recipe import Recipe
from foody_scraper.src.database.ingredient_dao import IngredientDao
from foody_scraper.src.database.mongo import Mongo
from foody_scraper.src.utils.pandas_utils import pandas_iter


class AprioriAnalyser:
    MAX_INGREDIENTS: int = 20
    MIN_SUUPPORT = 0.003
    MIN_CONFIDENCE = 0.2
    MIN_LIFT = 3
    MIN_LENGTH = 2
    MAX_LENGTH = 2

    def __init__(self):
        self.mongo = Mongo()
        self.ingredientDao = IngredientDao()
        pass

    def prepare_ingredient_matrix(self, recipes: List[Recipe]) -> List[List[str]]:
        ingredients_matrix = []

        for recipe in recipes:
            ingredients_row = []
            n_ingredients = len(recipe['ingredients'])

            for i in range(0, self.MAX_INGREDIENTS):
                if i < n_ingredients:
                    ingredients_row.append(str(recipe['ingredients'][i]['id']))
                else:
                    ingredients_row.append('nan')

            ingredients_matrix.append(ingredients_row)

        return ingredients_matrix

    def execute_apriori(self):
        recipes = self.mongo.find_all()
        ingredients_matrix = self.prepare_ingredient_matrix(recipes)

        ingredients_rulers = list(apriori(transactions=ingredients_matrix, min_support=self.MIN_SUUPPORT,
                                          min_confidence=self.MIN_CONFIDENCE, min_lift=self.MIN_LIFT,
                                          min_length=self.MIN_LENGTH, max_length=self.MAX_LENGTH))

        ingredients_rulers_df = pd.DataFrame(self.inspect(ingredients_rulers),
                                          columns=['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift'])
        top_ingredients_rulers_df = ingredients_rulers_df.nlargest(n=2*len(ingredients_matrix), columns='Lift')

        for left, right, support, confidence, lift in pandas_iter(top_ingredients_rulers_df, ['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence', 'Lift']):
            for recipe in recipes:
                ingredients_id = {str(ingredient['id']) for ingredient in recipe['ingredients']}
                if {left, right}.issubset(ingredients_id):
                    ingredients = [self.ingredientDao.find_by_id(int(left)),
                                   self.ingredientDao.find_by_id(int(right))]
                    self.mongo.set_good_combinations_for_recipe(
                        recipe,
                        GoodCombination(id=GoodCombination.generate_id(ingredients),
                                        ingredients=ingredients,
                                        support=support,
                                        confidence=confidence,
                                        lift=lift))

    @staticmethod
    def inspect(results):
        lhs = [tuple(result[2][0][0])[0] for result in results]
        rhs = [tuple(result[2][0][1])[0] for result in results]
        supports = [result[1] for result in results]
        confidences = [result[2][0][2] for result in results]
        lifts = [result[2][0][3] for result in results]

        return list(zip(lhs, rhs, supports, confidences, lifts))
