from pathlib import Path
import requests
import json
from datetime import datetime
from config import Config


# Multiple data sources can be added here
# RSS feeds and News APIs
def fetch_newsapi(query="technology", page_size=100):
    url = f"https://newsapi.org/v2/everything?q={query}&pageSize={page_size}&apiKey={Config.NEWS_API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data["articles"]


def put_newsapi(directory):
    news_api_data = fetch_newsapi()
    with open(f"{directory}/news_api_raw.json", "w") as file:
        json.dump(news_api_data, file, indent=4)
        file.close()


# def fetch_hackernews():
#     url = Config.HACKERNEWS_BASE_URL+"newstories.json"
#     response = requests.get(url)
#     items = response.json()[:20]
#     data = []
#     for item in items:
#         item_url = Config.HACKERNEWS_BASE_URL + f"item/{item}.json"
#         response = requests.get(item_url)
#         data.append(response.json())
#     return data
#
#
# def put_hackernews(directory):
#     hacker_news_data = fetch_hackernews()
#     with open(f"{directory}/hacker_news_raw.json", "w") as file:
#         json.dump(hacker_news_data, file, indent=4)
#         file.close()


if __name__ == "__main__":
    raw_directory = Path(Config.BASE_DIR) / 'data' / 'raw' / datetime.now().strftime("%Y%m%d%H%M%S")
    raw_directory.mkdir()
    put_newsapi(raw_directory)
    # put_hackernews(raw_directory)
