from bs4 import BeautifulSoup


class ReceiptPageParserTask:
    def get_receipt_title_from_soup(self, page_soup: BeautifulSoup) -> str:
        raw_title = page_soup.findAll('h1', 'recipe__name g-h1')

        return raw_title[0].text.strip() if raw_title else ''
