import time
import requests
import pandas as pd
from bs4 import BeautifulSoup


def get_product_data(product_url):
    response = requests.get(product_url)
    html = response.text

    soup = BeautifulSoup(html, "lxml")
    
    product_title = soup.find("h1", class_="dVrDvy")
    product_price = soup.find("h4", class_="finalPrice")
    product_description = soup.find("div", id="description")
    
    product = {
        "title": product_title.text if product_title else None, 
        "price": product_price.text if product_price else None,
        "description": product_description.text if product_description else None,
    }

    return product


if __name__ == "__main__":
    url = "https://www.kabum.com.br/hardware/placa-de-video-vga?page_size=60"
    
    start_time = time.time()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    # Processando links da página
    product_urls = soup.find_all("a", class_="productLink")
    product_urls = [l.get("href") for l in product_urls]
    product_urls = [f"https://www.kabum.com.br{href}" for href in product_urls]

    products = []
    for product_url in product_urls:
        product = get_product_data(product_url)
        products.append(product)

    print(f"collected data for {len(products)} products in {time.time() - start_time:.2f} seconds")

    df = pd.DataFrame.from_records(products)
    df.to_csv("kabum_simple.csv", index=False)

    print(df.head())