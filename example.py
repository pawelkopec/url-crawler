import json

from urlcrawler.Crawler import Crawler

crawler = Crawler()

google_tree = crawler.search_active_urls(
    "http://fanjet.pl", logs=True,)

print(json.dumps(google_tree, sort_keys=True, indent=2))
