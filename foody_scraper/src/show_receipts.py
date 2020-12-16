import asyncio
from pprint import pprint

from foody_scraper.src.database.mongo import Mongo


def find(f, seq):
    """Return first item in sequence where f(item) == True."""
    for item in seq:
        if f(item):
            return item


async def main():
    mongo = Mongo()
    receipts = mongo.find_all()
    popular_ingredients = []
    pprint(receipts)
    for recipe_dict in receipts:

        # Getting good combinations
        good_combinations = recipe_dict['good_combinations']
        if len(good_combinations) > 0:
            for combination in good_combinations:
                ingredients = combination['ingredients']
                if len(ingredients) > 0:

                    # Update popular combinations or add new
                    existed_combination = find(lambda comb: comb['ingredients'] == ingredients, popular_ingredients)
                    if existed_combination is None:
                        popular_ingredients.append({"ingredients": ingredients, "count": 0})
                    else:
                        index = popular_ingredients.index(existed_combination)
                        popular_ingredients[index]['count'] = existed_combination['count'] + 1

    pprint(sorted(popular_ingredients, key=lambda i: i['count']))


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
