class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if not root or root.key == key:
            return root

        if root.key > key:  # key is in left subtree
            if not root.left:
                return root

            if root.left.key > key:  # zig-zig (left-left)
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)
            elif root.left.key < key:  # zig-zag (left-right)
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            if not root.left:
                return root
            return self._rotate_right(root)

        else:  # key is in right subtree
            if not root.right:
                return root

            if root.right.key < key:  # zag-zag (right-right)
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)
            elif root.right.key > key:  # zag-zig (right-left)
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            if not root.right:
                return root
            return self._rotate_left(root)

    def insert(self, key, value):
        if not self.root:
            self.root = Node(key, value)
            return

        self.root = self._splay(self.root, key)

        if self.root.key == key:
            self.root.value = value  # Update existing value
            return

        new_node = Node(key, value)

        if self.root.key > key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None

        self.root = new_node

    def find(self, key):
        if not self.root:
            return None

        self.root = self._splay(self.root, key)

        if self.root.key != key:
            return None

        return self.root.value

    def __contains__(self, key):
        if not self.root:
            return False

        self.root = self._splay(self.root, key)
        return self.root.key == key