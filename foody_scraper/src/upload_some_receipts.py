import asyncio

from foody_scraper.src.scraper.scraper import Scraper


async def main():
    scraper_task = Scraper()
    for i in range(1, 3):
        await scraper_task.load_receipts_from_page(i)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
