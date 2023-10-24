import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

def get_movie_summaries(url):
    summaries_url = f'{url}plotsummary'
    print(summaries_url)
    response = requests.get(summaries_url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')

    data_to_store = []
    
    summaries_containers = soup.find("div", attrs={'data-testid': 'sub-section-summaries'})
    if summaries_containers is not None:
        summaries = summaries_containers.find_all('div', class_="ipc-html-content-inner-div")
        for summary in summaries:
            summary_dict = {'url': url, 'type':'summary', 'content': summary.text}
            data_to_store.append(summary_dict)

    synopsis_containers = soup.find("div", attrs={'data-testid': 'sub-section-synopsis'})
    if synopsis_containers is not None:
        synopsises = synopsis_containers.find_all('div', class_="ipc-html-content-inner-div")
        for synopsis in synopsises:
            synopsis_dict = {'url': url, 'type':'synopsis', 'content': synopsis.text}
            data_to_store.append(synopsis_dict)

    return data_to_store

if __name__ == "__main__":
    movies = pd.read_csv('search_results.csv')
    movies = movies.iloc[:10]

    start_time = time.time()
    all_summaries = []
    for _, row in movies.iterrows():
        url = row['url']
        summaries = get_movie_summaries(url)
        all_summaries.extend(summaries)

    print(f"Time taken: {time.time() - start_time:.2f} seconds")

    df = pd.DataFrame(all_summaries)
    df.to_csv('movie_summaries.csv', index=False)
    print(df.head())