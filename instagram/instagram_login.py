import re
import requests
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')

LOGIN_PAGE_URL = "https://www.instagram.com/accounts/login/"
LOGIN_API_URL = "https://www.instagram.com/api/v1/web/accounts/login/ajax/"
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0'


def fetch_csrf_token(session):
    response = session.get(LOGIN_PAGE_URL)
    csrf_pattern = r'\\"csrf_token\\":\\"([^"]+)'
    match = re.search(csrf_pattern, response.text)

    csrf_token = match.group(1) if match else None
    if not csrf_token:
        raise ValueError("CSRF token not found.")
    
    return csrf_token


if __name__ == "__main__":
    headers = {
            "user-agent": USER_AGENT,
            "x-requested-with": "XMLHttpRequest",
            "referer": LOGIN_PAGE_URL,
            "x-csrftoken": None,
        }

    timestamp = int(datetime.now().timestamp())
    encrypted_password = f"#PWD_INSTAGRAM_BROWSER:0:{timestamp}:{PASSWORD}"

    print(USERNAME, encrypted_password)

    payload = {
        "username": USERNAME,
        "enc_password": encrypted_password,
        "queryParams": {},
        "optIntoOneTap": "false",
    }

    session = requests.Session()
    
    csrf_token = fetch_csrf_token(session)
    headers["x-csrftoken"] = csrf_token

    print(f"Found CSRF token: {csrf_token}")

    response = session.post(LOGIN_API_URL, data=payload, headers=headers)

    sessionid = session.cookies.get("sessionid")
    if sessionid is not None:
        print(f"Authenticated successfully as {USERNAME}. Session ID: {sessionid[:7]}")
    else:
        print(f"Could not authenticate as {USERNAME}.")