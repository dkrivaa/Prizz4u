import asyncio

from crawling import crawl_to_get_links
from extraction import extract_data_from_link, make_store_list


async def main():
    """
    This function serves as subprocess to get a printout of stores list
    """
    # Getting list of stores download file using crawl4ai
    stores_gz_url_list = await crawl_to_get_links(get_prices=False)
    # Using the url to extract the data in file
    stores_data = await extract_data_from_link(stores_gz_url_list[0], price_data=False)
    # Making list of stores from extracted data
    stores_list = await make_store_list(stores_data)
    print(stores_list)


if __name__ == "__main__":
    asyncio.run(main())

