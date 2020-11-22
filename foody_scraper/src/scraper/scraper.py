import asyncio
import random

import aiohttp
from bs4 import BeautifulSoup

from foody_scraper.src.data.recipe import Recipe
from foody_scraper.src.database.mongo import Mongo
from foody_scraper.src.scraper.api_constants import *
from .receipt_link_parser import ReceiptLinkParser
from .receipt_parser import RecipePageParser


class Scraper:
    def __init__(self):
        self.recipe_page_parser = RecipePageParser()
        self.links_page_parser = ReceiptLinkParser()
        self.mongo = Mongo()
        #self.mongo.drop()

    async def get_receipts(self) -> None:
        is_end = []
        current_page = 1
        page_offset = 10

        while not is_end:
            is_end = [result._result for result in (await asyncio.wait([
                self.load_receipts_from_page(page_number)
                for page_number in range(current_page, current_page + page_offset)]))[0] if result._result]

            current_page += page_offset

    async def load_receipts_from_page(self, page_number):
        print(f'Started loading for page: {page_number}')
        receipt_links = await self.get_receipt_links(page_number)

        if len(receipt_links) == 0:
            print(f'The last page is {page_number - 1}')
            return True

        is_existed = [result._result for result in (await asyncio.wait([self.update_receipts(receipt_link)
                                                                        for receipt_link in receipt_links]))[0] if result._result]

        if is_existed:
            print('The record already exists in the database!\nThe process of scraping is interrupted!')
            return True

        print(f'Finished page: {page_number}')
        return False

    async def update_receipts(self, receipt_link: str) -> bool:
        receipt_from_db: Recipe = self.mongo.find_by_link(receipt_link)
        if receipt_from_db:
            return True
        await asyncio.sleep(random.randint(1, 6))

        self.mongo.save((await self.get_receipt(receipt_link)))
        return False

    async def get_receipt_links(self, page_number: int):
        links_page_url = EDA_URL + '/recepty?page=' + str(page_number)
        async with aiohttp.ClientSession() as session:
            response = await session.get(links_page_url)
            soup = BeautifulSoup(await response.text(), 'html.parser')
            await session.close()
        return self.links_page_parser.get_links(soup)

    async def get_receipt(self, receipt_link: str) -> Recipe:
        async with aiohttp.ClientSession() as session:
            response = await session.get(receipt_link)
            soup = BeautifulSoup(await response.text(), 'html.parser')
            await session.close()
        recipe_title = self.recipe_page_parser.get_recipe_title_from_soup(soup)
        recipe_time = self.recipe_page_parser.get_recipe_time_from_soup(soup)
        recipe_n_persons = self.recipe_page_parser.get_recipe_n_persons_from_soup(soup)
        recipe_image_link = self.recipe_page_parser.get_recipe_image_link(soup)
        ingredients = self.recipe_page_parser.get_ingredients_from_soup(soup)
        tags = self.recipe_page_parser.get_tags_from_soup(soup)
        nutritions = self.recipe_page_parser.get_nutrition_list_from_soup(soup)
        recipe_steps = self.recipe_page_parser.get_recipe_steps(soup)

        return Recipe(
            link=receipt_link,
            image_link=recipe_image_link,
            title=recipe_title,
            time=recipe_time,
            n_persons=recipe_n_persons,
            ingredients=ingredients,
            tags=tags,
            nutritions=nutritions,
            recipe_steps=recipe_steps
        )
