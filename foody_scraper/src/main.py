import asyncio
import sys, os

from foody_scraper.src.scraper.scraper import Scraper



async def main():
    scraper_task = Scraper()
    await scraper_task.get_receipts()


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
