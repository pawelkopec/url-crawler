from html.parser import HTMLParser

# a class for finding resources of given domain
# on an html page like links and images

class ServerPathFinder(HTMLParser):

    def __init__(self, domain):
        HTMLParser.__init__(self)
        self.domain = domain
        self.paths = []

    def feed(self, data):
        self.paths = []
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        path = None

        if tag == 'a' or tag == 'link':
            for attr in attrs:
                if attr[0] == 'href':
                    path = attr[1]
                    break

        if tag == 'img':
            for attr in attrs:
                if attr[0] == 'src':
                    path = attr[1]
                    break

        if path is not None:
            if path.startswith(self.domain):
                self.paths.append(path[len(self.domain):])
            elif path.startswith('/'):
                self.paths.append(path)

    def error(self, message):
        pass
