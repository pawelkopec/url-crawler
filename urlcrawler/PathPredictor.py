
# an abstract class for providing a crawler with new paths
# e.g. via machine learning or fixed statistical models

class PathPredictor(object):

    def feed(self, path, valid):
       pass

    def draw(self):
        pass

    def has_paths(self):
        pass
