from typing import List


class ScraperTask:
    def get_receipts(self):
        receipts = {}

        for page_number in range(1, 2):
            receipt_links = self.get_receipt_links(page_number)
            for receipt_link in receipt_links:
                receipts[receipt_link] = self.get_receipt(receipt_link)

        return receipts

    def get_receipt_links(self, page_number: int) -> List[str]:
        return ['https://eda.ru/recepty/osnovnye-blyuda/bigos-16752']

    def get_receipt(self, receipt_link: str):
        pass
