import os
import json

def append_article_to_master_json(article: dict, filename=None) -> None:
    """
    Appends a single article to a shared JSON file outside scraper/.
    Automatically assigns a unique ID.
    """
    assert isinstance(article, dict), "Article must be a dictionary."

    # Set path to save in project root (../articles.json)
    if filename is None:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(base_dir, "articles.json")

    data = []

    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, list), "File must contain a list of articles."
        except (json.JSONDecodeError, AssertionError):
            print("⚠️ Warning: Could not read existing file. Starting fresh.")
            data = []

    next_id = 1 if not data else max(a.get("id", 0) for a in data) + 1
    article_with_id = {"id": next_id, **article}
    data.append(article_with_id)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print(f"✅ Article saved with ID {next_id} in '{filename}'")
