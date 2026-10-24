TOPIC = {
    "id": "trees",
    "title": "Binary Trees & BSTs",
    "category": "Trees & Graphs",
    "summary": "Traversals, recursion on trees, and binary search trees.",
    "visualizer": "bst",
    "lesson": """
A **binary tree** is made of nodes where each node has at most two children, `left` and `right`. The top node is the **root**; nodes with no children are **leaves**.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
```

`TreeNode` is predefined in this site's problems. Tests describe trees in **level order**, with `None` for missing children: `[3, 9, 20, None, None, 15, 7]`.

## Traversals

- **Pre-order** (node, left, right): copy a tree, serialize it.
- **In-order** (left, node, right): on a BST this visits values **in sorted order**.
- **Post-order** (left, right, node): compute things that depend on children, like height or deleting a tree.
- **Level-order (BFS)**: visit level by level using a queue.

```python
def inorder(node):
    if node:
        inorder(node.left)
        print(node.val)
        inorder(node.right)
```

## Thinking recursively

Most tree problems follow one shape: *solve for the left subtree, solve for the right subtree, combine.* For example the height is `1 + max(height(left), height(right))`, with height `0` for `None`.

## Binary search trees (BST)

A BST keeps the rule: **everything in the left subtree < node < everything in the right subtree**. Searching, inserting and deleting walk one path from the root, so they take `O(h)`, where `h` is the height. That's `O(log n)` when the tree is balanced, and `O(n)` when it degenerates into a line (e.g. inserting sorted data).
""",
    "complexity": [
        {"operation": "Traverse all nodes", "time": "O(n)", "space": "O(h)"},
        {"operation": "BST search / insert / delete (balanced)", "time": "O(log n)", "space": "O(h)"},
        {"operation": "BST search / insert / delete (skewed)", "time": "O(n)", "space": "O(n)"},
        {"operation": "Level-order traversal", "time": "O(n)", "space": "O(width)"},
        {"operation": "Height of tree", "time": "O(n)", "space": "O(h)"},
    ],
    "snippets": [
        {
            "title": "BST insert and search",
            "code": r'''class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def insert(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insert(root.left, val)
    else:
        root.right = insert(root.right, val)
    return root


def contains(root, val):
    while root:
        if val == root.val:
            return True
        root = root.left if val < root.val else root.right
    return False


root = None
for v in [8, 3, 10, 1, 6, 14]:
    root = insert(root, v)
print(contains(root, 6), contains(root, 7))  # True False
''',
        },
        {
            "title": "Level-order traversal with a queue",
            "code": r'''from collections import deque


def level_order(root):
    if not root:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels
''',
        },
    ],
    "problems": [
        {
            "id": "max-depth-binary-tree",
            "title": "Maximum Depth of Binary Tree",
            "difficulty": "Easy",
            "statement": """
Return the number of nodes along the longest path from the root down to a leaf.

**Example**

```
    3
   / \\
  9  20
     / \\
    15  7        ->  3
```
""",
            "function": "max_depth",
            "arg_types": ["tree"],
            "starter": "def max_depth(root):\n    pass\n",
            "tests": [
                {"args": [[3, 9, 20, None, None, 15, 7]], "expected": 3},
                {"args": [[1, None, 2]], "expected": 2},
                {"args": [[]], "expected": 0},
                {"args": [[1, 2, None, 3, None, 4]], "expected": 4},
            ],
            "hints": ["depth(node) = 1 + max(depth(left), depth(right)); depth(None) = 0."],
            "solution": r'''def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
''',
        },
        {
            "id": "invert-binary-tree",
            "title": "Invert Binary Tree",
            "difficulty": "Easy",
            "statement": """
Mirror the tree (swap every node's left and right children) and return its root.

**Example**

```
[4, 2, 7, 1, 3, 6, 9]  ->  [4, 7, 2, 9, 6, 3, 1]
```
""",
            "function": "invert_tree",
            "arg_types": ["tree"],
            "return_type": "tree",
            "starter": "def invert_tree(root):\n    pass\n",
            "tests": [
                {"args": [[4, 2, 7, 1, 3, 6, 9]], "expected": [4, 7, 2, 9, 6, 3, 1]},
                {"args": [[2, 1, 3]], "expected": [2, 3, 1]},
                {"args": [[]], "expected": []},
                {"args": [[1, 2]], "expected": [1, None, 2]},
            ],
            "hints": ["Swap the children of the current node, then invert each subtree."],
            "solution": r'''def invert_tree(root):
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
''',
        },
        {
            "id": "validate-bst",
            "title": "Validate Binary Search Tree",
            "difficulty": "Medium",
            "statement": """
Return `True` if the tree is a valid BST: for every node, all values in its left subtree are strictly smaller and all values in its right subtree are strictly larger.

**Example**

```
[2, 1, 3]                     ->  True
[5, 1, 4, None, None, 3, 6]   ->  False   (3 is in 5's right subtree)
```
""",
            "function": "is_valid_bst",
            "arg_types": ["tree"],
            "starter": "def is_valid_bst(root):\n    pass\n",
            "tests": [
                {"args": [[2, 1, 3]], "expected": True},
                {"args": [[5, 1, 4, None, None, 3, 6]], "expected": False},
                {"args": [[5, 4, 6, None, None, 3, 7]], "expected": False},
                {"args": [[1]], "expected": True},
                {"args": [[2, 2, 2]], "expected": False},
            ],
            "hints": [
                "Checking only a node against its direct children isn't enough.",
                "Pass down a valid (low, high) range: going left tightens high, going right tightens low.",
            ],
            "solution": r'''def is_valid_bst(root, low=float("-inf"), high=float("inf")):
    if root is None:
        return True
    if not low < root.val < high:
        return False
    return (is_valid_bst(root.left, low, root.val)
            and is_valid_bst(root.right, root.val, high))
''',
        },
        {
            "id": "level-order-traversal",
            "title": "Level Order Traversal",
            "difficulty": "Medium",
            "statement": """
Return the node values level by level, left to right, as a list of lists.

**Example**

```
[3, 9, 20, None, None, 15, 7]  ->  [[3], [9, 20], [15, 7]]
```
""",
            "function": "level_order",
            "arg_types": ["tree"],
            "starter": "def level_order(root):\n    pass\n",
            "tests": [
                {"args": [[3, 9, 20, None, None, 15, 7]], "expected": [[3], [9, 20], [15, 7]]},
                {"args": [[1]], "expected": [[1]]},
                {"args": [[]], "expected": []},
                {"args": [[1, 2, 3, 4, None, None, 5]], "expected": [[1], [2, 3], [4, 5]]},
            ],
            "hints": [
                "Use a deque as a queue.",
                "Process exactly `len(queue)` nodes per level before moving on.",
            ],
            "solution": r'''from collections import deque


def level_order(root):
    if root is None:
        return []
    levels, queue = [], deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        levels.append(level)
    return levels
''',
        },
    ],
    "quiz": [
        {
            "question": "Which traversal visits a BST's values in sorted order?",
            "options": ["Pre-order", "In-order", "Post-order", "Level-order"],
            "answer": 1,
            "explanation": "Left subtree (smaller), node, right subtree (larger).",
        },
        {
            "question": "What is the time to search a balanced BST with n nodes?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
            "answer": 1,
            "explanation": "Each comparison discards one subtree; a balanced tree has height ≈ log n.",
        },
        {
            "question": "Inserting 1, 2, 3, 4, 5 in order into an empty BST produces…",
            "options": ["A balanced tree", "A tree shaped like a linked list", "An error", "A heap"],
            "answer": 1,
            "explanation": "Each value goes to the right of the previous one, so height becomes n.",
        },
        {
            "question": "Which data structure does level-order traversal use?",
            "options": ["Stack", "Queue", "Hash map", "Heap"],
            "answer": 1,
            "explanation": "FIFO order processes all nodes at depth d before depth d + 1.",
        },
        {
            "question": "What is the height of an empty tree, with height(leaf) = 1?",
            "options": ["-1", "0", "1", "Undefined"],
            "answer": 1,
            "explanation": "The base case height(None) = 0 makes the recursion work.",
        },
    ],
}
