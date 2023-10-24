import time
import aiohttp
import asyncio
import requests
import pandas as pd
from bs4 import BeautifulSoup


async def fetch_all_products(product_urls):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(
            *[get_product_data(product_url, session) for product_url in product_urls]
        )


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
    }


async def fetch_html(url, session, params = None):
    async with session.get(url, params=params) as response:
        response.raise_for_status()
        return await response.text()


if __name__ == "__main__":
    url = "https://www.kabum.com.br/hardware/placa-de-video-vga?page_size=60"
    
    start_time = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    product_urls = soup.find_all("a", class_="productLink")
    product_urls = [l.get("href") for l in product_urls]
    product_urls = [f"https://www.kabum.com.br{href}" for href in product_urls]

    products = asyncio.run(fetch_all_products(product_urls))

    print(f"collected data for {len(products)} products in {time.time() - start_time:.2f} seconds")

    df = pd.DataFrame.from_records(products)
    df.to_csv("kabum_simple_async.csv", index=False)

    print(df.head())