
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from foody_scraper.src.data.receipt import Receipt
from .receipt_parser import ReceiptPageParser


class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.receipt_page_parser = ReceiptPageParser()

    def get_receipts(self) -> Dict[str, Receipt]:
        receipts = {}

        for page_number in range(1, 2):
            receipt_links = self.get_receipt_links(page_number)
            for receipt_link in receipt_links:
                receipts[receipt_link] = self.get_receipt(receipt_link)

        return receipts

    def get_receipt_links(self, page_number: int) -> List[str]:
        return ['https://eda.ru/recepty/osnovnye-blyuda/bigos-16752']

    def get_receipt(self, receipt_link: str) -> Receipt:
        receipt_page = self.session.get(receipt_link)
        soup = BeautifulSoup(receipt_page.text, 'html.parser')

        receipt_title = self.receipt_page_parser.get_receipt_title_from_soup(soup)
        receipt_time = self.receipt_page_parser.get_receipt_time_from_soup(soup)
        receipt_n_persons = self.receipt_page_parser.get_receipt_n_persons_from_soup(soup)
        ingredients = self.receipt_page_parser.get_ingredients_from_soup(soup)
        tags = self.receipt_page_parser.get_tags_from_soup(soup)

        return Receipt(
            title=receipt_title,
            time=receipt_time,
            n_persons=receipt_n_persons,
            ingredients=ingredients,
            tags=tags
        )