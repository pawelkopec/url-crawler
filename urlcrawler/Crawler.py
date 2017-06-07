from threading import Lock, active_count, Thread

import requests
from requests.exceptions import RequestException

from urlcrawler.ServerPathFinder import ServerPathFinder
from urlcrawler.UrlTree import UrlTree


class Crawler(object):

    def __init__(self):
        self.lock = Lock()

    def search_active_urls(self, domain, paths=None, path_predictor=None,
                           max_threads=10,  timeout=1, logs=False):
        domain = self.normalize_domain(domain)

        tree = UrlTree()

        if paths is None:
            paths = []

        paths = [''] + paths

        if logs:
            print('Started searching domain {}\n'.format(domain))

        self.crawl_loop_func(domain, paths, tree, path_predictor,
                             max_threads, timeout, logs)

        return tree.as_dict()

    def crawl_loop_func(self, domain, paths, tree,
                           path_predictor, max_threads, timeout, logs):
        not_in_use = set(paths)
        path = paths.pop()
        while True:

            while max_threads == active_count():
                pass

            args = (domain, path, paths, not_in_use, tree, path_predictor, timeout,
                    logs)

            Thread(target=self.crawl, args=args).start()

            while True:
                self.lock.acquire()

                if paths:
                    path = paths.pop()
                    self.lock.release()

                    path = self.preprocess_path(path, paths, not_in_use, tree)
                    if path is not None:
                        break
                else:
                    self.lock.release()

                if active_count() == 1:
                    if not paths:
                        return

            if not paths and path_predictor is not None:
                if path_predictor.has_paths():
                    paths.append(path_predictor.draw())

    def preprocess_path(self, path, paths, not_in_use, tree):
        path = self.normalize_path(path)

        delimiters = [i for i, c in enumerate(path) if c == '/']

        if delimiters:
            for d in delimiters[1:]:
                new_path = path[:d]
                self.lock.acquire()
                if new_path not in not_in_use:
                    paths.append(new_path)
                    not_in_use.add(new_path)
                self.lock.release()

        if tree.has_code_for_path(path):
            return None

        return path

    def crawl(self, domain, path, paths, not_in_use, tree, path_predictor,
              timeout, logs):

        try:
            head = requests.head(domain + path, timeout=timeout)
            code = head.status_code

            if code in self.INVALID_CODES:
                if path_predictor:
                    path_predictor.feed(path, False)
                if tree.contains_path(path):
                    tree.add_code_for_path(path, code)
            else:
                if path_predictor:
                    path_predictor.feed(path, True)

                tree.add_code_for_path(path, code)

                if logs:
                    print('Successfully found resource under {}'
                          .format(path or '/'))

                found_paths = self.find_new_paths(head, domain, path, timeout)

                if found_paths is not None:
                    for found_path in found_paths:
                        self.lock.acquire()

                        if found_path not in not_in_use:
                            paths.append(found_path)
                            not_in_use.add(found_path)

                        self.lock.release()

        except RequestException as e:
            if logs:
                print('\nSearching aborted for resource {} :\n\t{}\n'
                      .format(path, e))
        except UnicodeDecodeError as e:
            if logs:
                print('\nText analysing aborted for resource {} :\n\t{}\n'
                      .format(path, e))

    def find_new_paths(self, head, domain, path, timeout):
        try:
            if not self.has_xml_based_resource(head):
                return None

            response = requests.get(domain + path, timeout=timeout)

            if response.apparent_encoding is None:
                return None

            finder = ServerPathFinder(domain)
            finder.feed(response.content.decode(response.apparent_encoding))

            return finder.paths

        except UnicodeDecodeError as e:
            raise e

    @staticmethod
    def has_xml_based_resource(head):
        content_type = head.headers.get("content-type")

        if content_type:
            return "text/html" in content_type or \
                   "text/xml" in content_type

        return False

    @staticmethod
    def normalize_domain(domain):
        if domain[-1] == '/':
            return domain[:-1]

        return domain

    @staticmethod
    def normalize_path(path):
        if not path:
            return ''
        if path[0] != '/':
            path = '/' + path
        if path[-1] == '/':
            path = path[:-1]

        return path

    INVALID_CODES = [404, 500, 501, 502, 503, 504,
                     505, 506, 507, 508, 510, 511]