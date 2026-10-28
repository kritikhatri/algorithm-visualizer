TOPIC = {
    "id": "union-find",
    "title": "Union-Find (Disjoint Sets)",
    "category": "Trees & Graphs",
    "summary": "Merge groups and ask 'are these connected?' in nearly O(1).",
    "visualizer": "union-find",
    "lesson": """
**Union-Find** (also called *Disjoint Set Union*, DSU) keeps track of items split into groups. It supports two operations:

- `find(x)`: which group is `x` in? Returns the group's **root** (representative).
- `union(a, b)`: merge the groups containing `a` and `b`.

Two items are connected exactly when `find(a) == find(b)`.

## How it's stored

Every item points to a **parent**; a root points to itself. A group is a little tree, and `find` follows parents up to the root.

```python
parent = list(range(n))        # everyone starts alone

def find(x):
    while parent[x] != x:
        x = parent[x]
    return x
```

## Two optimizations that make it fast

1. **Path compression:** while finding the root, point nodes directly at it, so the next lookup is one hop.
2. **Union by size (or rank):** attach the smaller tree under the larger one, keeping trees shallow.

Together they make each operation run in **amortized O(α(n))**, where α is the inverse Ackermann function: below 5 for any realistic input, so effectively constant.

```python
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])   # path compression
    return parent[x]

def union(a, b):
    ra, rb = find(a), find(b)
    if ra == rb:
        return False                  # already connected: a cycle edge!
    if size[ra] < size[rb]:
        ra, rb = rb, ra
    parent[rb] = ra
    size[ra] += size[rb]
    return True
```

## When to reach for it

- Counting **connected components** as edges arrive
- **Detecting cycles** in an undirected graph (a union that finds both ends already joined)
- **Kruskal's** minimum spanning tree
- Grouping equivalent things: accounts with shared emails, equal variables, similar strings
""",
    "complexity": [
        {"operation": "find / union (both optimizations)", "time": "O(α(n)) ≈ O(1)", "space": "O(n)"},
        {"operation": "find without optimizations (worst)", "time": "O(n)", "space": "O(n)"},
        {"operation": "Process E edges", "time": "O(E · α(n))", "space": "O(n)"},
    ],
    "snippets": [
        {
            "title": "A reusable DSU class",
            "code": r'''class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        self.groups = n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.groups -= 1
        return True


d = DSU(6)
for a, b in [(0, 1), (1, 2), (3, 4)]:
    d.union(a, b)
print(d.groups, d.find(2) == d.find(0), d.find(5) == d.find(4))  # 3 True False
''',
        },
        {
            "title": "Kruskal's minimum spanning tree",
            "code": r'''def kruskal(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = 0
    for w, a, b in sorted(edges):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            total += w
    return total


print(kruskal(4, [(1, 0, 1), (4, 0, 2), (3, 1, 2), (2, 1, 3), (5, 2, 3)]))  # 6
''',
        },
    ],
    "problems": [
        {
            "id": "count-components-dsu",
            "title": "Number of Connected Components",
            "difficulty": "Medium",
            "statement": """
There are `n` nodes `0..n-1` and an undirected edge list. Return the number of connected components.

**Example**

```
count_components(5, [[0, 1], [1, 2], [3, 4]])  ->  2
```
""",
            "function": "count_components",
            "starter": "def count_components(n, edges):\n    pass\n",
            "tests": [
                {"args": [5, [[0, 1], [1, 2], [3, 4]]], "expected": 2},
                {"args": [5, [[0, 1], [1, 2], [2, 3], [3, 4]]], "expected": 1},
                {"args": [3, []], "expected": 3},
                {"args": [4, [[0, 1], [1, 0], [2, 3]]], "expected": 2},
            ],
            "hints": ["Start with n groups; every union that actually merges two groups reduces the count by one."],
            "solution": r'''def count_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    groups = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra
            groups -= 1
    return groups
''',
        },
        {
            "id": "redundant-connection",
            "title": "Redundant Connection",
            "difficulty": "Medium",
            "statement": """
A tree of nodes `1..n` had one extra edge added, creating exactly one cycle. Return the edge that can be removed to make it a tree again; if several work, return the one that appears **last** in `edges`.

**Example**

```
find_redundant_connection([[1, 2], [1, 3], [2, 3]])  ->  [2, 3]
```
""",
            "function": "find_redundant_connection",
            "starter": "def find_redundant_connection(edges):\n    pass\n",
            "tests": [
                {"args": [[[1, 2], [1, 3], [2, 3]]], "expected": [2, 3]},
                {"args": [[[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]], "expected": [1, 4]},
                {"args": [[[1, 2], [2, 3], [1, 3], [3, 4]]], "expected": [1, 3]},
            ],
            "hints": ["Union edges in order. The first edge whose two ends are already connected closes the cycle."],
            "solution": r'''def find_redundant_connection(edges):
    parent = list(range(len(edges) + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return [a, b]
        parent[rb] = ra
''',
        },
        {
            "id": "satisfiable-equations",
            "title": "Satisfiability of Equality Equations",
            "difficulty": "Medium",
            "statement": """
Each string in `equations` looks like `"a==b"` or `"a!=b"` with single lowercase letters. Return `True` if you can assign integers to the letters so all equations hold.

**Example**

```
equations_possible(["a==b", "b!=a"])  ->  False
equations_possible(["a==b", "b==c", "a==c"])  ->  True
```
""",
            "function": "equations_possible",
            "starter": "def equations_possible(equations):\n    pass\n",
            "tests": [
                {"args": [["a==b", "b!=a"]], "expected": False},
                {"args": [["b==a", "a==b"]], "expected": True},
                {"args": [["a==b", "b==c", "a==c"]], "expected": True},
                {"args": [["a==b", "b!=c", "c==a"]], "expected": False},
                {"args": [["a!=a"]], "expected": False},
            ],
            "hints": [
                "First union every pair joined by ==.",
                "Then check that no != pair ended up in the same group.",
            ],
            "solution": r'''def equations_possible(equations):
    parent = {ch: ch for ch in "abcdefghijklmnopqrstuvwxyz"}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for eq in equations:
        if eq[1:3] == "==":
            parent[find(eq[0])] = find(eq[3])
    return all(find(eq[0]) != find(eq[3]) for eq in equations if eq[1:3] == "!=")
''',
        },
    ],
    "quiz": [
        {
            "question": "What does find(x) return?",
            "options": ["x's parent", "The root (representative) of x's group", "The group size", "True or False"],
            "answer": 1,
            "explanation": "Two items are connected exactly when their roots are equal.",
        },
        {
            "question": "What does path compression do?",
            "options": [
                "Deletes unused nodes",
                "Points nodes on the find path directly at the root",
                "Sorts the parent array",
                "Merges all groups",
            ],
            "answer": 1,
            "explanation": "Future finds on those nodes become a single hop.",
        },
        {
            "question": "With union by size, which tree goes under which?",
            "options": [
                "The larger under the smaller",
                "The smaller under the larger",
                "Always the first argument's tree",
                "It doesn't matter",
            ],
            "answer": 1,
            "explanation": "Keeping the bigger tree's root keeps trees shallow.",
        },
        {
            "question": "union(a, b) finds both already have the same root. In an undirected graph, this edge…",
            "options": ["Is a bridge", "Creates a cycle", "Disconnects the graph", "Is a self-loop"],
            "answer": 1,
            "explanation": "a and b were already connected, so adding the edge closes a loop.",
        },
        {
            "question": "Amortized cost of find/union with both optimizations?",
            "options": ["O(n)", "O(log n)", "O(α(n)), effectively constant", "O(n²)"],
            "answer": 2,
            "explanation": "The inverse Ackermann function grows so slowly it's below 5 in practice.",
        },
    ],
    "flashcards": [
        {"front": "The two Union-Find operations?", "back": "find(x): root of x's group. union(a, b): merge a's and b's groups."},
        {"front": "How do you initialise a DSU for n items?", "back": "parent = list(range(n)): everyone is their own root."},
        {"front": "The two DSU optimizations?", "back": "Path compression (point nodes at the root) and union by size/rank (attach smaller under larger)."},
        {"front": "How does DSU detect a cycle?", "back": "When union(a, b) finds find(a) == find(b): the edge connects already-connected nodes."},
        {"front": "Classic DSU applications?", "back": "Connected components, cycle detection, Kruskal's MST, grouping equivalent items."},
    ],
}
