import requests
from requests.exceptions import RequestException

from urlcrawler.ServerPathFinder import ServerPathFinder
from urlcrawler.UrlTree import UrlTree


class Crawler(object):

    def search_active_urls(self, domain, paths=None,
                           path_predictor=None, timeout=1, logs=False):
        domain = self.normalize_domain(domain)

        tree = UrlTree()

        if paths is None:
            paths = []

        paths = [''] + paths

        if logs:
            print('Started searching domain {}\n'.format(domain))

        self.crawl_loop_func(domain, paths, tree, path_predictor, timeout, logs)

        return tree.as_dict()

    def crawl_loop_func(self, domain, paths, tree,
                           path_predictor, timeout, logs):
        while paths:
            while paths:
                self.crawl(domain, paths.pop(), paths, tree, path_predictor,
                           timeout, logs)

            if paths and path_predictor is not None:
                if path_predictor.has_paths():
                    paths.append(path_predictor.draw())

    def crawl(self, domain, path, paths, tree, path_predictor, timeout, logs):
        path = self.normalize_path(path)

        delimiters = [i for i, c in enumerate(path) if c == '/']

        for d in delimiters:
            paths.append(path[:d])

        if tree.has_code_for_path(path):
            return

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
                        if found_path not in paths:
                            paths.append(found_path)

        except (RequestException, UnicodeDecodeError) as e:
            if logs:
                print('\nSearching aborted for resource {} :\n\t{}\n'
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
