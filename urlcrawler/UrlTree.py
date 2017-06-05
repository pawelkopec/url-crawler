
class UrlTree(object):

    def __init__(self):
        self.root = {'children': {}}

    def get_node_for_path(self, path):
        nodes = self.path_to_nodes(path)
        current_leaf = self.root

        for i in range(len(nodes)):
            if nodes[i] not in current_leaf.get('children'):
                return None

            current_leaf = current_leaf.get('children')[nodes[i]]

        return current_leaf

    def contains_path(self, path):
        return self.get_node_for_path(path) is not None

    def has_code_for_path(self, path):
        leaf = self.get_node_for_path(path)

        if leaf is None:
            return False

        return leaf.get('response-code') is not None

    def add_code_for_path(self, path, code):
        leaves = self.path_to_nodes(path)
        current_parent = self.root

        for i in range(len(leaves)):
            if leaves[i] in current_parent.get('children'):
                current_parent = current_parent.get('children')[leaves[i]]
            else:
                for j in range(i, len(leaves) - 1):
                    new_parent = {
                        'children': {},
                        'response-code': None
                    }

                    current_parent.get('children')[leaves[j]] = new_parent
                    current_parent = new_parent

                new_child = {
                    'children': {},
                    'response-code': code
                }

                current_parent.get('children')[leaves[-1]] = new_child

                return

        current_parent['response-code'] = code

    def as_dict(self):
        hidden_root = self.root.get('children').get('')

        if hidden_root:
            tree = hidden_root.copy()
            self.remove_none_keys(tree)

            return tree

        return {}

    def remove_none_keys(self, node):
        if not node.get('response-code'):
            node.pop('response-code', None)

        for child in node.get('children').values():
            self.remove_none_keys(child)

        if len(node.get('children')) == 0:
            node.pop('children', None)

    @staticmethod
    def path_to_nodes(path):
        return [''] + path.split('/')[1:]
