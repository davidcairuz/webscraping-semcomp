import requests
import pandas as pd

class InstagramConfig:
    """
    Contains the configuration settings and constants required for querying Instagram.
    """
    BASE_URL = 'https://www.instagram.com/graphql/query/'

    COOKIES = {
        'ig_did': '738F4349-891A-4ADB-824F-F5DE4E3615DE',
        'datr': 'SNI3ZSnySWrz0lUR2PxVGNFF',
        'csrftoken': 'gXO4wRzRpAmaGJmlWwxWabZ3eCqSCGge',
        'mid': 'ZTfSSQAEAAELx7XWvAUarDqPhXlf',
        'ig_nrcb': '1',
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
    }

    PARAMETERS = {
        'doc_id': '17991233890457762',
        'variables': '{"id":"8229168335","after":"","first":20}',
    }


def fetch_user_posts(end_cursor=""):
    """
    Fetches posts of a user from Instagram.
    """
    variables = f'{{"id":"8229168335","after":"{end_cursor}","first":20}}'
    response = requests.get(
        InstagramConfig.BASE_URL,
        params={**InstagramConfig.PARAMETERS, "variables": variables},
        cookies=InstagramConfig.COOKIES,
        headers=InstagramConfig.HEADERS
    )
    return response.json()


def extract_post_data(post_node):
    """
    Extracts post details from a post node. Save only photos.
    """
    post_data = post_node["node"]
    post_details = {
        'id': post_data['id'],
        'shortcode': post_data['shortcode'],
        'timestamp': post_data['taken_at_timestamp'],
        'likes': post_data['edge_media_preview_like']['count'],
        'comments': post_data['edge_media_to_comment']['count'],
        'caption': post_data['edge_media_to_caption']['edges'][0]['node'].get("text", "") if post_data['edge_media_to_caption']['edges'] else "",
        'is_video': post_data['is_video'],
        'display_url': post_data['display_url'] if not post_data['is_video'] else None
    }

    return post_details if not post_details['is_video'] else None


def extract_pagination_info(content):
    """
    Extracts pagination information (whether there's a next page and the end cursor).
    """
    page_info = content['data']['user']['edge_owner_to_timeline_media']['page_info']
    return page_info['has_next_page'], page_info['end_cursor']


def main():
    all_posts = []
    has_next_page, end_cursor = True, ""

    while has_next_page:
        content = fetch_user_posts(end_cursor=end_cursor)
        posts_on_page = content['data']['user']['edge_owner_to_timeline_media']['edges']

        for post_node in posts_on_page:
            post = extract_post_data(post_node)
            if post:
                all_posts.append(post)

        has_next_page, end_cursor = extract_pagination_info(content)
        print(f"Scraped {len(all_posts)} posts")

    df = pd.DataFrame(all_posts)
    df.to_csv('instagram_posts.csv', index=False)


if __name__ == "__main__":
    main()
