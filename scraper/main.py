from scraper_core import (
    fetch_article_html,
    extract_title_from_html,
    extract_author_from_html,
    extract_date_from_html,
    extract_article_body
)

def scrape_single_post():
    url = "https://www.newyorker.com/news/the-weekend-essay/how-to-save-a-dog"
    html = fetch_article_html(url)
    print(f"Fetched {len(html)} characters of HTML.")

    title = extract_title_from_html(html)
    print(f"Article title: {title}")

    author = extract_author_from_html(html)
    print(f"Author: {author}")

    date = extract_date_from_html(html)
    print(f"Published: {date}")

    content = extract_article_body(html)
    print("\n--- Article Content ---\n")
    print(content[:1000])

if __name__ == "__main__":
    scrape_single_post()
