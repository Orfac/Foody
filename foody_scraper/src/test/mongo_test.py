import dataclasses
from pprint import pprint

from pymongo import MongoClient

from foody_scraper.src.data.ingredient import Ingredient
from foody_scraper.src.data.measure import Measure
from foody_scraper.src.data.nutrition import Nutrition
from foody_scraper.src.data.recipe import Recipe
from foody_scraper.src.database.mongo import Mongo


title = "Борщ"
measure = Measure(
    title="столовая ложка",
    normal_title_form="лол кек",
    amount=5.0
)
ingredient = Ingredient(
    id=1,
    name="Петрушка",
    measure=measure
)
nutrition = Nutrition(
    name="example",
    measure=measure
)
recipe = Recipe(
    link='test_link',
    image_link='image_link',
    title=title,
    time="time",
    n_persons=1,
    ingredients=[ingredient],
    tags=["вкусный", "классный"],
    nutritions=[nutrition],
    recipe_steps=["бульон", "ещё что-то"]
)

mongo = Mongo()
mongo.drop()
recipes = mongo.recipes
mongo.save(recipe)

print("\nSearch all: \n")
pprint(mongo.find_all())
print("\nSearch by title: \n\n")
pprint(mongo.find_by_title(title))
print("\nSearch by title wrong title: \n\n")
pprint(mongo.find_by_title("Неверный борщ"))

