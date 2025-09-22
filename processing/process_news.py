from config import Config
import pandas as pd
import json
from pathlib import Path


def get_latest_raw_directory(base_dir):
    raw_data_dir = Path(base_dir) / 'data' / 'raw'
    subdirectories = [d for d in raw_data_dir.iterdir() if d.is_dir()]
    if not subdirectories:
        raise FileNotFoundError(f"No subdirectories found in {raw_data_dir}")
    latest_directory = sorted(subdirectories, key=lambda x: x.name, reverse=True)[0]
    return latest_directory


def find_json_file(directory):
    for file in directory.glob("*.json"):
        return file
    raise FileNotFoundError(f"No JSON file found in {directory}")


def process_news(json_file):
    with open(json_file, "r") as f:
        articles = json.load(f)
    df = pd.json_normalize(articles)
    df = df[["source.name", "author", "title", "description", "publishedAt", "url"]]
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])
    df.drop_duplicates(subset=["url"], inplace=True)
    return df


if __name__ == "__main__":
    latest_dir = get_latest_raw_directory(Config.BASE_DIR)
    json_file = find_json_file(latest_dir)
    df_processed = process_news(json_file)

    processed_dir = Path(Config.BASE_DIR) / 'data' / 'processed' / latest_dir
    processed_dir.mkdir(parents=True, exist_ok=True)
    df_processed.to_csv(processed_dir / "processed_news.csv", index=False)
