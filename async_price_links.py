import asyncio
import sys
import re
from datetime import datetime
from collections import defaultdict

from crawling import crawl_to_get_links


# If the return urls list has 5 files (sometimes happens)
def get_timestamp_from_url(url):
    # Match YYYYMMDDHHMM in the filename
    match = re.search(r'(\d{12})\.gz', url)
    if match:
        return datetime.strptime(match.group(1), "%Y%m%d%H%M")
    return None

def get_file_type(url):
    # Extract file type from path (e.g., price, pricefull, promo, promofull)
    match = re.search(r'blob\.core\.windows\.net/([^/]+)/', url)
    return match.group(1) if match else None

def deduplicate_urls(urls):
    grouped = defaultdict(list)

    # Group by file type
    for url in urls:
        file_type = get_file_type(url)
        if file_type:
            grouped[file_type].append(url)

    final_urls = []
    for file_type, url_list in grouped.items():
        if not url_list:
            continue
        # Select the newest URL by timestamp
        latest_url = max(url_list, key=get_timestamp_from_url)
        final_urls.append(latest_url)

    if len(final_urls) != 4:
        raise ValueError(f"Expected 4 unique file types, but found {len(final_urls)}. Check input.")

    return final_urls


async def main():
    """
    This function serves as subprocess to get a printout of selected store prices
    """
    # Getting list of price download files using Crawl4ai
    store_code = sys.argv[1]
    prices_gz_url_list = await crawl_to_get_links(get_prices=True, store_code=store_code)
    if len(prices_gz_url_list) == 4:
        for url in prices_gz_url_list:
            print(url)

    # If urls list have 5 links
    elif len(prices_gz_url_list) == 5:
        urls_list = deduplicate_urls(prices_gz_url_list)
        for url in urls_list:
            print(url)


if __name__ == "__main__":
    asyncio.run(main())
