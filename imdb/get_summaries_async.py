import pandas as pd
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
}

async def get_movie_summaries(session, url):
    summaries_url = f'{url}plotsummary'
    print(summaries_url)
    async with session.get(summaries_url, headers=headers) as response:
        html = await response.text()
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

async def main(movie_urls):
    async with aiohttp.ClientSession() as session:
        tasks = [get_movie_summaries(session, url) for url in movie_urls]
        return await asyncio.gather(*tasks)

if __name__ == "__main__":
    movies = pd.read_csv('search_results.csv')
    movie_urls = movies['url'].tolist()[:1000]

    print(f"Collecting data for {len(movie_urls)} movies")
    start_time = time.time()
    movie_data = asyncio.run(main(movie_urls))

    all_summaries = [item for sublist in movie_data for item in sublist]

    print(f"Time taken: {time.time() - start_time:.2f} seconds")

    df = pd.DataFrame(all_summaries)
    df.to_csv('movie_summaries.csv', index=False)
    print(df.head())
