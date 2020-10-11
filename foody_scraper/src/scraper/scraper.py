
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from foody_scraper.src.data.receipt import Receipt
from .receipt_link_parser import ReceiptLinkParser
from .receipt_parser import ReceiptPageParser
from foody_scraper.src.scraper.api_constants import *

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.receipt_page_parser = ReceiptPageParser()
        self.links_page_parser = ReceiptLinkParser()

    def get_receipts(self) -> Dict[str, Receipt]:
        receipts = {}

        for page_number in range(1, 2):
            receipt_links = self.get_receipt_links(page_number)
            for receipt_link in receipt_links:
                receipts[receipt_link] = self.get_receipt(receipt_link)

        return receipts

    def get_receipt_links(self, page_number: int) -> List[str]:
        links_page_url = EDA_URL + "/recepty?page=" + str(page_number)
        links_page = self.session.get(links_page_url)
        soup = BeautifulSoup(links_page.text, 'html.parser')
        return self.links_page_parser.get_links(soup)

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