from foody_scraper.src.scraper.scraper_task import ScraperTask


def main():
    scraper_task = ScraperTask()
    scraper_task.get_receipts()


if __name__ == '__main__':
    main()