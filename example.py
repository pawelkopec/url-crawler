import json

from urlcrawler.Crawler import Crawler

crawler = Crawler()

google_tree = crawler.get_website_tree(
    "http://google.com", logs=True)

print(json.dumps(google_tree, sort_keys=True, indent=2))
