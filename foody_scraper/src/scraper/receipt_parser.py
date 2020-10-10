import json
from typing import Any, Optional

from bs4 import BeautifulSoup

from foody_scraper.src.data.ingredient import IngredientConverter


class ReceiptPageParser:
    def __init__(self):
        self.ingredient_converter = IngredientConverter()

    def get_receipt_title_from_soup(self, page_soup: BeautifulSoup) -> Optional[str]:
        raw_title = page_soup.findAll('h1', 'recipe__name g-h1')

        return raw_title[0].text.strip() if raw_title else ''

    def get_receipt_time_from_soup(self, page_soup: BeautifulSoup) -> Optional[str]:
        data = self.__get_important_from_info_pad(page_soup, 1)
        return data

    def get_receipt_n_persons_from_soup(self, page_soup: BeautifulSoup) -> Optional[int]:
        data = self.__get_important_from_info_pad(page_soup, 0)

        return int(data) if data else data

    def get_ingredients_from_soup(self, page_soup: BeautifulSoup):
        raw_ingredients_list = page_soup.findAll('div', 'ingredients-list__content')
        if not raw_ingredients_list:
            return None
        raw_ingredients = raw_ingredients_list[0].find_all('p', 'ingredients-list__content-item content-item js-cart-ingredients')
        ingredients = []

        for raw_ingredient in raw_ingredients:
            ingredient = json.loads(raw_ingredient['data-ingredient-object'])
            ingredients.append(self.ingredient_converter.get_from_dict(ingredient))

        return ingredients

    def get_tags_from_soup(self, page_soup: BeautifulSoup):
        raw_tag_list = page_soup.findAll('ul', 'breadcrumbs')
        if not raw_tag_list:
            return None

        raw_tags = raw_tag_list[0].find_all('a', '')
        tags = []
        for raw_tag in raw_tags:
            tags.append(raw_tag.text)

        return tags

    @staticmethod
    def __get_important_from_info_pad(page_soup:  BeautifulSoup, element_position: int) -> Optional[Any]:
        raw_info_pad = page_soup.findAll('div', 'recipe__info-pad info-pad print-invisible')
        if not raw_info_pad:
            return None

        raw_data = raw_info_pad[0].find_all('span', 'info-text')
        return raw_data[element_position].text.strip() if raw_data else None
