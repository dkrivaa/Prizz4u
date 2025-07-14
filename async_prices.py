import asyncio
import sys

from crawling import crawl_to_get_links
from extraction import extract_data_from_link


async def main():
    """
    This function serves as subprocess to get a printout of selected store prices
    """
    # Getting list of price download files using crawl4ai
    store_code = sys.argv[1]
    prices_gz_url_list = await crawl_to_get_links(get_prices=True, store_code=store_code)
    # Using the relevant url to extract the data in file - fullprice
    prices_data = await extract_data_from_link(prices_gz_url_list[1], price_data=True)
    print(prices_data)


if __name__ == "__main__":
    asyncio.run(main())

