from foody_scraper.src.scraper.scraper import Scraper


def main():
    scraper_task = Scraper()
    scraper_task.get_receipts()


if __name__ == '__main__':
    main()