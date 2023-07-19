from collections import deque


class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.__class__.__name__}({self.val})"


class BinaryTree:
    def __init__(self, iterable):
        if not iterable:
            self.nodes = []
            self.size = 0
            self.root = None
        else:
            self.nodes = [TreeNode(i) if i is not None else None for i in iterable]
            self.size = len(self.nodes)
            self.root = self.nodes[0]
            self.__build_from_nodes()

    def __build_from_nodes(self):
        nodes = self.nodes
        size = self.size
        for idx in range(size):
            if nodes[idx] is None:
                continue
            left_idx = 2 * idx + 1
            right_idx = left_idx + 1
            nodes[idx].left = nodes[left_idx] if left_idx < size else None
            nodes[idx].right = nodes[right_idx] if right_idx < size else None

    def collect_in_level_order(self):
        nodes = {}
        if self.root is None:
            return nodes

        def dfs(cur, depth=1):
            if not cur:
                return
            nodes.setdefault(depth, []).append(cur.val)
            if cur.left:
                dfs(cur.left, depth + 1)
            if cur.right:
                dfs(cur.right, depth + 1)
        dfs(self.root)
        return nodes

    def traverse_in_level_order(self):
        vals = []
        if self.root is None:
            return vals

        dq = deque([self.root])
        while dq:
            cur = dq.popleft()
            vals.append(cur.val)
            if cur.left:
                dq.append(cur.left)
            if cur.right:
                dq.append(cur.right)
        return vals


if __name__ == "__main__":
    print(BinaryTree([]).collect_in_level_order())

    tree = BinaryTree([0, 1, 2, 3, 4, 5, 6, None, 8, 9, 10])
    print(tree.nodes[3], tree.nodes[3].left, tree.nodes[3].right)
    print(tree.collect_in_level_order())
    print(tree.traverse_in_level_order())
