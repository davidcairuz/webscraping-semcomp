import aiohttp
import asyncio
import pandas as pd
import time

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

async def fetch_pokemon(session, pokemon):
    async with session.get(BASE_URL + pokemon) as response:
        return await response.json()

async def main(pokemon_list):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_pokemon(session, pokemon) for pokemon in pokemon_list]
        return await asyncio.gather(*tasks)


if __name__ == "__main__":
    df = pd.read_csv("pokemon.csv")
    pokemon_list = df["identifier"].tolist()[:100]
    
    print(f"collecting data for {len(pokemon_list)} pokemon")
    start_time = time.time()
    pokemon_data = asyncio.run(main(pokemon_list))
    
    type_counter = {}
    for data in pokemon_data:
        pokemon_type = data["types"][0]["type"].get("name")
        type_counter[pokemon_type] = type_counter.get(pokemon_type, 0) + 1
    
    print(f"took {time.time() - start_time:.2f} seconds")
    print(type_counter)
