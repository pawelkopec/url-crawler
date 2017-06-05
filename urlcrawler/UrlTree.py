
class UrlTree(object):

    def __init__(self):
        self.root = {'children': []}

    def get_node_for_path(self, path):
        nodes = self.path_to_nodes(path)
        current_node = self.root

        for i in range(len(nodes)):
            if not self.has_child_for_name(current_node, nodes[i]):
                return None

            current_node = self.get_child_by_name(current_node, nodes[i])

        return current_node

    def contains_path(self, path):
        return self.get_node_for_path(path) is not None

    def has_code_for_path(self, path):
        node = self.get_node_for_path(path)

        if node is None:
            return False

        return node.get('response-code') is not None

    def add_code_for_path(self, path, code):
        nodes = self.path_to_nodes(path)
        current_parent = self.root

        for i in range(len(nodes)):
            if self.has_child_for_name(current_parent, nodes[i]):
                current_parent = self.get_child_by_name(current_parent, nodes[i])
            else:
                for j in range(i, len(nodes) - 1):
                    new_parent = {
                        'name': nodes[j],
                        'response-code': None,
                        'children': []
                    }

                    current_parent.get('children').append(new_parent)
                    current_parent = new_parent

                new_child = {
                    'name': nodes[-1],
                    'response-code': code,
                    'children': []
                }

                current_parent.get('children').append(new_child)

                return

        current_parent['response-code'] = code

    def as_dict(self):
        hidden_root = self.get_child_by_name(self.root, self.ROOT_DUMMY)

        if hidden_root:
            tree = hidden_root.copy()
            self.remove_none_keys(tree)

            return tree

        return {}

    def remove_none_keys(self, node):
        if not node.get('response-code'):
            node.pop('response-code', None)

        for child in node.get('children'):
            self.remove_none_keys(child)

        if len(node.get('children')) == 0:
            node.pop('children', None)

    def get_child_by_name(self, node, name):
        for child in node.get('children'):
            if child.get('name') == name:
                return child

        return None

    def has_child_for_name(self, node, name):
        return self.get_child_by_name(node, name) is not None

    def path_to_nodes(self, path):
        return [self.ROOT_DUMMY] + path.split('/')[1:]

    ROOT_DUMMY = ''
