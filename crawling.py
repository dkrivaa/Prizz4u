from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
import asyncio


async def crawl_to_get_links(get_prices: bool = True, store_code: str = '134'):
    """
    This function gets either:
    1 - the latest links for store file or
    2 - the latest links for price files for specified store
    from Shufersal price transparency website.
    """
    if get_prices:
        # JS_code to select prices
        select_code = f"""
            (() => {{
                    const dropdown = document.querySelector('#ddlStore');
                    dropdown.value = {str(store_code)};
                    dropdown.dispatchEvent(new Event('change'));    
            }})() 
            """
    else:
        # JS_code to select the stores option
        select_code = """
                (() => {
                        const dropdown = document.querySelector('#ddlCategory');
                        dropdown.value = '5';
                        dropdown.dispatchEvent(new Event('change'));    
                })() 
                """

    browser_config = BrowserConfig(
        headless=True,
    )

    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        js_code=select_code,
        delay_before_return_html=2.5,
        session_id="hn_session"
    )

    next_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        delay_before_return_html=10,
        # Mark that we do not re-navigate, but run JS in the same session:
        js_only=True,
        session_id="hn_session"
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        # The first run - selecting the stores option
        result = await crawler.arun(
            url='https://prices.shufersal.co.il',
            config=run_config
        )
        # The second run - get download links
        result2 = await crawler.arun(
            url='https://prices.shufersal.co.il',
            config=next_config
        )

        return [d['href'] for d in result2.links.get('external', [])]


links = asyncio.run(crawl_to_get_links(get_prices=True))
print(links)
