import requests
import os
from dotenv import load_dotenv

load_dotenv()

IP_CHECK_URL = "https://api64.ipify.org?format=json"

def create_proxy():
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    proxy_address = f"http://{username}:{password}@gate.smartproxy.com:7000"
    proxy = {
        "http": proxy_address,
        "https": proxy_address,
    }

    return proxy


def check_current_ip(proxy):
    response = requests.get(IP_CHECK_URL, proxies=proxy)
    if response.status_code == 200:
        return response.json().get("ip")
    else:
        return None
    
if __name__ == "__main__":
    proxy_info = create_proxy()
    current_ip = check_current_ip(proxy_info)

    if current_ip:
        print(f"Current IP address: {current_ip}")
    else:
        print("Failed to retrieve the current IP using the proxy.")
