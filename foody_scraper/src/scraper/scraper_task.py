from dataclasses import dataclass
from typing import List, Any, Dict
from bs4 import BeautifulSoup
import requests

from .receipt_parser_task import ReceiptPageParserTask


@dataclass
class Receipt:
    title: str


class ScraperTask:
    def __init__(self):
        self.session = requests.Session()
        self.receipt_page_scraper = ReceiptPageParserTask()

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

        receipt_title = self.receipt_page_scraper.get_receipt_title_from_soup(soup)

        return Receipt(title=receipt_title)