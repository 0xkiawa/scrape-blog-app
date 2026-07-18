"""
Config for headline-only scraping.

Each site entry defines WHERE to look for headlines (a section/homepage
listing many articles, not a single article page) and HOW to find them
(a CSS-ish strategy handled generically in headline_scraper.py).

NOTE: We intentionally never fetch or store full article bodies here.
Titles + links + source are all we need to spot a trending topic.
"""

SITES = [
    {
        "name": "NYT",
        "url": "https://www.nytimes.com/section/culture",
    },
    {
        "name": "Washington Post",
        "url": "https://www.washingtonpost.com/opinions/",
    },
    {
        "name": "New Yorker",
        "url": "https://www.newyorker.com/culture",
    },
    {
        "name": "New York Post",
        "url": "https://nypost.com/entertainment/",
    },
    {
        "name": "The Atlantic",
        "url": "https://www.theatlantic.com/culture/",
    },
    {
        "name": "Slate",
        "url": "https://slate.com/culture",
    },
]

# Words too common to count as a "trending keyword" on their own.
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "in", "on", "at", "to", "for",
    "with", "by", "from", "is", "are", "was", "were", "be", "been", "being",
    "it", "its", "this", "that", "these", "those", "how", "why", "what",
    "who", "whom", "which", "when", "where", "as", "into", "about", "after",
    "before", "over", "under", "than", "then", "so", "if", "not", "no", "yes",
    "up", "down", "out", "off", "again", "just", "new", "york", "times",
    "post", "opinion", "culture", "review", "says", "say", "said", "one",
    "two", "his", "her", "their", "our", "your", "my", "i", "he", "she",
    "they", "we", "you", "will", "can", "could", "should", "would", "has",
    "have", "had", "did", "do", "does", "s", "nobody", "everyone", "someone",
    "everything", "something", "anyone", "coming", "suddenly", "inside",
    "talking", "ready", "rise", "asked", "still", "even", "also", "more",
    "most", "much", "many", "every", "all", "get", "gets", "getting", "got",
    "make", "makes", "making", "made", "like", "way", "ways", "here", "there",
    "now", "today", "week", "year", "years", "back", "first", "last", "own",
}