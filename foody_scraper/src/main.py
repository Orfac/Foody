from foody_scraper.src.scraper.scraper import Scraper


def main():
    scraper_task = Scraper()
    receipts = scraper_task.get_receipts()
    for recipe in receipts:
        print(receipts[recipe])


if __name__ == '__main__':
    main()