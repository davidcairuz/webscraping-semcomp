from concurrent.futures import ThreadPoolExecutor
import requests
import pandas as pd
import time

BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

def fetch_pokemon(pokemon):
    response = requests.get(BASE_URL + pokemon)
    return response.json()

if __name__ == "__main__":
    df = pd.read_csv("pokemon.csv")
    pokemon_list = df["identifier"].tolist()[:100]
    
    print(f"collecting data for {len(pokemon_list)} pokemon")
    
    start_time = time.time()
    with ThreadPoolExecutor() as executor:
        pokemon_data = list(executor.map(fetch_pokemon, pokemon_list))
    
    type_counter = {}
    for data in pokemon_data:
        pokemon_type = data["types"][0]["type"].get("name")
        type_counter[pokemon_type] = type_counter.get(pokemon_type, 0) + 1
    
    print(f"took {time.time() - start_time:.2f} seconds")
    print(type_counter)