import aiohttp
import asyncio
import requests
import pandas as pd
from time import time
from loguru import logger
from bs4 import BeautifulSoup

PRODUCT_PAGE_PARAMS = {
    "page_number": 1,
    "page_size": 100,
    "facet_filters": "",
    "sort": "most_searched",
}

async def get_all_product_urls(base_url):
    base_url = base_url.split("?")[0]
    total_pages = await get_total_pages(base_url)
    
    async with aiohttp.ClientSession() as session:
        response_data = await asyncio.gather(
            *[get_page_urls(base_url, page_number, session) for page_number in range(1, total_pages + 1)]
        )
    return [url for sublist in response_data for url in sublist]


async def get_total_pages(base_url):
    response = requests.get(base_url, params=PRODUCT_PAGE_PARAMS)
    soup = BeautifulSoup(response.text, "lxml")
    return int(soup.find_all("a", class_="page")[-1].text)


async def get_page_urls(base_url, page_number, session):
    params = PRODUCT_PAGE_PARAMS.copy()
    params["page_number"] = page_number
    
    html = await fetch_html(base_url, session, params)
    soup = BeautifulSoup(html, "lxml")
    
    page_urls = [p.get("href") for p in soup.find_all("a", class_="productLink")]
    page_urls = [f"https://www.kabum.com.br{url}" for url in page_urls]
    return page_urls


async def fetch_html(url, session, params=None):
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.text()
    

async def get_product_data(product_url, session):
    html = await fetch_html(product_url, session)
    soup = BeautifulSoup(html, "lxml")

    product_title = soup.find("h1", class_="dVrDvy")
    product_price = soup.find("h4", class_="finalPrice")
    product_description = soup.find("div", id="description")

    return {
        "title": product_title.text if product_title else None,
        "price": product_price.text if product_price else None,
        "description": product_description.text if product_description else None,
        "url": product_url,
        "in_stock": product_price is not None
    }


async def fetch_all_products(product_urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[get_product_data(product_url, session) for product_url in product_urls]
        )


if __name__ == "__main__":
    product_base_url = "https://www.kabum.com.br/cameras-e-drones"
    
    logger.info(f"Starting to collect all product links from {product_base_url}")
    start_time = time()
    product_urls = asyncio.run(get_all_product_urls(product_base_url))
    elapsed_time = time() - start_time
    logger.info(f"Collected {len(product_urls)} product links in {elapsed_time:.2f} seconds")

    logger.info(f"Starting to collect data for {len(product_urls)} products")
    start_time = time()
    products = asyncio.run(fetch_all_products(product_urls))
    elapsed_time = time() - start_time
    logger.info(f"Collected data for {len(products)} products in {elapsed_time:.2f} seconds")

    logger.info("Saving products to CSV")
    df = pd.DataFrame.from_records(products)
    df.to_csv("kabum.csv", index=False)
    
    logger.debug(f"\n{df.head()}")
