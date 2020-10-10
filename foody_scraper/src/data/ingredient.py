from dataclasses import dataclass
from typing import Dict, Any

from foody_scraper.src.data.measure import Measure
from foody_scraper.src.data_analysis.language_analyser import LanguageAnalyser


@dataclass
class Ingredient:
    id: int
    name: str
    measure: Measure


class IngredientConverter:
    def __init__(self):
        self.language_analyser = LanguageAnalyser()

    def get_from_dict(self, ingredient_dict: Dict[str, Any]):
        id = ingredient_dict['id']
        name = ingredient_dict['name']
        if ingredient_dict['amount'].lower() != 'по вкусу':
            splitted_amount = ingredient_dict['amount'].split()
            amount = splitted_amount[0]
            title = self.apply_measure_pattern(' '.join(splitted_amount[1:]))
            normal_title_form = self.language_analyser.get_normal_form(title)
        else:
            title = 'по вкусу'
            normal_title_form = 'по вкусу'
            amount = '-1'

        return Ingredient(
            id=id,
            name=name,
            measure=Measure(title=title, normal_title_form=normal_title_form, amount=float(amount))
        )

    @staticmethod
    def apply_measure_pattern(measure_title):
        if measure_title == 'г':
            return 'гр'
        return measure_title
