import requests
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
    url = "https://www.kabum.com.br/produto/470309/placa-de-video-geforce-x3w-rtx-3070-8gb-ax-1755mhz-gddr6-hdmi-dp-3-lhr"
    product = get_product_data(url)

    print(product)