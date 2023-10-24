from google.cloud import pubsub_v1
from concurrent import futures
import json
from typing import Callable
import pandas as pd

GCP_PROJECT_ID = "imdb-dataset-1"
PUBSUB_TOPIC_ID = "url-movie-summary"

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(GCP_PROJECT_ID, PUBSUB_TOPIC_ID)
publish_futures = []

movies = pd.read_csv('search_results.csv')
movies = movies.iloc[:10]

def get_callback(
    publish_future: pubsub_v1.publisher.futures.Future, data: str
) -> Callable[[pubsub_v1.publisher.futures.Future], None]:
    def callback(publish_future: pubsub_v1.publisher.futures.Future) -> None:
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback

for _, row in movies.iterrows():
    url = row['url']
    message_body = {"url":url}
    data = json.dumps(message_body, indent=4)
    
    # When you publish a message, the client returns a future.
    publish_future = publisher.publish(topic_path, data.encode("utf-8"))
    # Non-blocking. Publish failures are handled in the callback function.
    publish_future.add_done_callback(get_callback(publish_future, data))
    publish_futures.append(publish_future)

# Wait for all the publish futures to resolve before exiting.
futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)
print(f"Published messages with error handler to {topic_path}.")