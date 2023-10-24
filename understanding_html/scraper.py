from bs4 import BeautifulSoup


def read_html_file(file_path):
    with open(file_path, "r") as html_file:
        return html_file.read()
    

def parse_article(article_div):
    article_title = article_div.h2.text
    article_summary = article_div.p.text
    article_url = article_div.a.get("href")

    print(f"====== Title: {article_title}")
    print(f"====== Summary: {article_summary}")
    print(f"====== URL: {article_url}\n\n")


if __name__ == "__main__":
    html = read_html_file("simple.html")
    soup = BeautifulSoup(html, "lxml")

    # acessando dessa forma, obtemos sempre a primeira ocorrencia da tag
    title = soup.title

    # find permite a busca por qualquer tag, classe, id, etc
    div = soup.find("div", class_= "footer")

    article_divs = soup.find_all("div", class_="article")
    for article_div in article_divs:
        parse_article(article_div)