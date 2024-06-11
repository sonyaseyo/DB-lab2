class Node:
    def __init__(self):
        self.keys = []
        self.parent = None


class Leaf(Node):
    def __init__(self):
        super().__init__()
        self.records = []
        self.next = None


class InternalNode(Node):
    def __init__(self):
        super().__init__()
        self.children = []


class BPlusTree:
    def __init__(self, order=4):
        self.root = Leaf()
        self.order = order

    def insert(self, key, value, contact_phone):
        node = self.root

        while isinstance(node, InternalNode):
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            node = node.children[i]

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            node.records[i].append((value, contact_phone))
        else:
            node.keys.insert(i, key)
            node.records.insert(i, [(value, contact_phone)])

        if len(node.keys) > self.order:
            self.split_leaf(node)

    def split_leaf(self, leaf):
        new_leaf = Leaf()
        mid = len(leaf.keys) // 2

        new_leaf.keys = leaf.keys[mid:]
        new_leaf.records = leaf.records[mid:]
        leaf.keys = leaf.keys[:mid]
        leaf.records = leaf.records[:mid]

        if leaf.next:
            new_leaf.next = leaf.next
        leaf.next = new_leaf

        new_leaf.parent = leaf.parent

        self.insert_internal(leaf.parent, leaf, new_leaf, new_leaf.keys[0])

    def insert_internal(self, parent, left_child, right_child, key):
        if parent is None:
            new_root = InternalNode()
            new_root.keys = [key]
            new_root.children = [left_child, right_child]
            self.root = new_root
            left_child.parent = new_root
            right_child.parent = new_root
            return

        i = 0
        while i < len(parent.keys) and key > parent.keys[i]:
            i += 1
        parent.keys.insert(i, key)
        parent.children.insert(i + 1, right_child)
        right_child.parent = parent

        if len(parent.keys) > self.order:
            self.split_internal(parent)

    def split_internal(self, node):
        new_node = InternalNode()
        mid = len(node.keys) // 2
        median_key = node.keys[mid]

        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]
        for child in new_node.children:
            child.parent = new_node

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if node == self.root:
            new_root = InternalNode()
            new_root.keys = [median_key]
            new_root.children = [node, new_node]
            self.root = new_root
            node.parent = new_root
            new_node.parent = new_root
        else:
            new_node.parent = node.parent
            self.insert_internal(node.parent, node, new_node, median_key)

    def search(self, key):
        node = self.root

        while isinstance(node, InternalNode):
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.records[i]

        return None

    def print_tree(self, node=None, indent=""):
        if node is None:
            node = self.root
        if isinstance(node, Leaf):
            print(indent + "Leaf: " + str(node.keys) + " " + str(node.records))
        else:
            print(indent + "Node: " + str(node.keys))
            for child in node.children:
                self.print_tree(child, indent + "  ")


names = ['Hanna', 'Liam', 'Violet', 'Xaden', 'Poppy', 'Jacks', 'Evangeline', 'Feyre', 'Rhysand', 'Cassian', 'Ava', 'Ben',
         'Damian', 'Gale', 'Irene', 'Kate', 'Mira', 'Nidalee', 'Qiqi', 'Sona', 'Taliyah', 'Yuna',
         'Zed']
phones = ['+38' + '0' * 5 + str(index + 1) for index in range(len(names))]

tree = BPlusTree()


def hash_name(name):
    name = name.lower()
    max_length = max([len(n) for n in names])
    hash_value = 0
    for i, char in enumerate(name):
        if i >= max_length:
            break
        hash_value += ord(char) ** (max_length - i - 1)

    return hash_value


for index, name in enumerate(names):
    hashed_name = hash_name(name)
    print(name, 'hash:', hashed_name)

for index, name in enumerate(names):
    hashed_name = hash_name(name)
    tree.insert(hashed_name, name, phones[index])

print('B+TREE:')
tree.print_tree()

name = 'Sona'
hashed_name = hash_name(name)
contact = tree.search(hashed_name)

if contact is not None:
    for i in contact:
        print(f'Name {i[0]} found. Phone: {i[1]}')
else:
    print(f'Name {name} is not found')
