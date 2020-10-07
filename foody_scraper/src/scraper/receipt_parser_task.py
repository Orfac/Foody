from typing import Any, Optional

from bs4 import BeautifulSoup


class ReceiptPageParserTask:
    def get_receipt_title_from_soup(self, page_soup: BeautifulSoup) -> Optional[str]:
        raw_title = page_soup.findAll('h1', 'recipe__name g-h1')

        return raw_title[0].text.strip() if raw_title else ''

    def get_receipt_time_from_soup(self, page_soup: BeautifulSoup) -> Optional[str]:
        data = self.__get_important_from_info_pad(page_soup, 1)
        return data

    def get_receipt_n_persons_from_soup(self, page_soup: BeautifulSoup) -> Optional[int]:
        data = self.__get_important_from_info_pad(page_soup, 0)

        return int(data) if data else data

    @staticmethod
    def __get_important_from_info_pad(page_soup:  BeautifulSoup, element_position: int) -> Optional[Any]:
        raw_info_pad = page_soup.findAll('div', 'recipe__info-pad info-pad print-invisible')
        if not raw_info_pad:
            return None

        raw_data = raw_info_pad[0].find_all('span', 'info-text')
        return raw_data[element_position].text.strip() if raw_data else None
