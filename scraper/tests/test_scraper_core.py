# scraper/tests/test_scraper_core.py

import unittest
from scraper_core import (
    extract_title_from_html,
    extract_author_from_html,
    extract_date_from_html,
    extract_article_body
)

MOCK_HTML = """
<html>
  <head>
    <title>Mock Title</title>
    <meta name="author" content="Test Author" />
    <meta property="article:published_time" content="2024-01-15T12:00:00Z" />
  </head>
  <body>
    <article>
      <p>This is the first paragraph.</p>
      <p>This is the second paragraph.</p>
    </article>
  </body>
</html>
"""

class TestScraperCore(unittest.TestCase):
    def test_title_extraction(self):
        self.assertEqual(extract_title_from_html(MOCK_HTML), "Mock Title")

    def test_author_extraction(self):
        self.assertEqual(extract_author_from_html(MOCK_HTML), "Test Author")

    def test_date_extraction(self):
        self.assertEqual(extract_date_from_html(MOCK_HTML), "2024-01-15T12:00:00Z")

    def test_article_body_extraction(self):
        body = extract_article_body(MOCK_HTML)
        self.assertIn("first paragraph", body)
        self.assertIn("second paragraph", body)

if __name__ == "__main__":
    unittest.main()
