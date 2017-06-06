import json
import time

from urlcrawler.Crawler import Crawler

crawler = Crawler()

times = []
for i in range(3, 12):
    start = time.time()
    google_tree = crawler.search_active_urls(
        "http://fanjet.pl", logs=True, max_threads=i)
    end = time.time()
    t = end - start
    times += [i, t]
    print('For ', i, ' threads: ', t, google_tree.get("active-paths"))

# for t in times:
#     print('For ', t[0], ' threads: ', t[1])

print(json.dumps(google_tree, sort_keys=True, indent=2))
