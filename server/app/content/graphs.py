TOPIC = {
    "id": "graphs",
    "title": "Graphs: BFS & DFS",
    "category": "Trees & Graphs",
    "summary": "Model connections, then explore them breadth-first or depth-first.",
    "visualizer": "graph",
    "lesson": """
A **graph** is a set of **vertices** (nodes) connected by **edges**. Graphs model road maps, social networks, course prerequisites, and grids.

- **Directed** edges go one way (`A → B`); **undirected** edges go both ways.
- **Weighted** edges carry a cost, like distance.

## Representing a graph in Python

The most common choice is an **adjacency list**: a dict from each node to its neighbours.

```python
from collections import defaultdict
graph = defaultdict(list)
for a, b in [(0, 1), (0, 2), (1, 3)]:
    graph[a].append(b)
    graph[b].append(a)     # undirected
```

A grid is a graph too: each cell's neighbours are up, down, left and right.

## Breadth-first search (BFS)

BFS explores in **waves**: first all nodes 1 edge away, then 2, and so on. It uses a **queue** and finds the **shortest path in an unweighted graph**.

```python
from collections import deque

def bfs(graph, start):
    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
```

## Depth-first search (DFS)

DFS goes **as deep as possible** before backing up. It uses recursion or an explicit **stack**. It's good for counting connected components, detecting cycles, and topological sorting.

## Always track visited nodes

Graphs can have cycles. Without a `seen` set, BFS/DFS will loop forever. Mark a node as seen **when you add it** to the queue/stack, not when you pop it, to avoid adding it twice.

## Topological sort

For a directed acyclic graph (DAG), a topological order lists every node before the nodes it points to, e.g. taking courses after their prerequisites. Kahn's algorithm repeatedly removes nodes with no incoming edges; if some nodes are never removed, there's a cycle.
""",
    "complexity": [
        {"operation": "BFS / DFS (adjacency list)", "time": "O(V + E)", "space": "O(V)"},
        {"operation": "Grid BFS / DFS (R × C)", "time": "O(R·C)", "space": "O(R·C)"},
        {"operation": "Topological sort (Kahn)", "time": "O(V + E)", "space": "O(V)"},
        {"operation": "Check edge (adjacency list)", "time": "O(degree)", "space": "—"},
        {"operation": "Adjacency matrix storage", "time": "—", "space": "O(V²)"},
    ],
    "snippets": [
        {
            "title": "Shortest path length with BFS",
            "code": r'''from collections import deque


def shortest_path(graph, start, goal):
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        node, dist = queue.popleft()
        if node == goal:
            return dist
        for nxt in graph.get(node, []):
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, dist + 1))
    return -1


g = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"]}
print(shortest_path(g, "A", "F"))  # 3
''',
        },
        {
            "title": "DFS: count connected components",
            "code": r'''def count_components(n, edges):
    graph = {i: [] for i in range(n)}
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    seen = set()

    def dfs(node):
        seen.add(node)
        for nxt in graph[node]:
            if nxt not in seen:
                dfs(nxt)

    components = 0
    for node in range(n):
        if node not in seen:
            dfs(node)
            components += 1
    return components


print(count_components(5, [(0, 1), (1, 2), (3, 4)]))  # 2
''',
        },
    ],
    "problems": [
        {
            "id": "number-of-islands",
            "title": "Number of Islands",
            "difficulty": "Medium",
            "statement": """
`grid` is a list of lists of `"1"` (land) and `"0"` (water). Count the islands: groups of land connected horizontally or vertically.

**Example**

```
[["1","1","0","0"],
 ["1","1","0","0"],
 ["0","0","1","0"],
 ["0","0","0","1"]]      ->  3
```
""",
            "function": "num_islands",
            "starter": "def num_islands(grid):\n    pass\n",
            "tests": [
                {"args": [[["1", "1", "0", "0"], ["1", "1", "0", "0"],
                           ["0", "0", "1", "0"], ["0", "0", "0", "1"]]], "expected": 3},
                {"args": [[["1", "1", "1"], ["0", "1", "0"], ["1", "1", "1"]]], "expected": 1},
                {"args": [[["0", "0"], ["0", "0"]]], "expected": 0},
                {"args": [[["1", "0", "1", "0", "1"]]], "expected": 3},
            ],
            "hints": [
                "Scan every cell. When you find unvisited land, that's a new island.",
                "Flood-fill (DFS or BFS) from it to mark the whole island as visited.",
            ],
            "solution": r'''def num_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = set()

    def sink(r, c):
        stack = [(r, c)]
        seen.add((r, c))
        while stack:
            r, c = stack.pop()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if (0 <= nr < rows and 0 <= nc < cols
                        and grid[nr][nc] == "1" and (nr, nc) not in seen):
                    seen.add((nr, nc))
                    stack.append((nr, nc))

    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in seen:
                sink(r, c)
                islands += 1
    return islands
''',
        },
        {
            "id": "course-schedule",
            "title": "Course Schedule",
            "difficulty": "Medium",
            "statement": """
There are `n` courses `0..n-1`. Each pair `[a, b]` in `prereqs` means you must take `b` before `a`. Return `True` if you can finish all courses (i.e. there is no cycle).

**Example**

```
can_finish(2, [[1, 0]])          ->  True
can_finish(2, [[1, 0], [0, 1]])  ->  False
```
""",
            "function": "can_finish",
            "starter": "def can_finish(n, prereqs):\n    pass\n",
            "tests": [
                {"args": [2, [[1, 0]]], "expected": True},
                {"args": [2, [[1, 0], [0, 1]]], "expected": False},
                {"args": [4, [[1, 0], [2, 1], [3, 2]]], "expected": True},
                {"args": [3, [[0, 1], [1, 2], [2, 0]]], "expected": False},
                {"args": [3, []], "expected": True},
            ],
            "hints": [
                "Build the graph b → a and count each course's incoming edges.",
                "Kahn's algorithm: repeatedly take courses with 0 remaining prerequisites. Did you take all n?",
            ],
            "solution": r'''from collections import deque


def can_finish(n, prereqs):
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for course, before in prereqs:
        graph[before].append(course)
        indegree[course] += 1

    queue = deque(i for i in range(n) if indegree[i] == 0)
    taken = 0
    while queue:
        course = queue.popleft()
        taken += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return taken == n
''',
        },
        {
            "id": "shortest-path-grid",
            "title": "Shortest Path in a Grid",
            "difficulty": "Medium",
            "statement": """
`grid` contains `0` (open) and `1` (wall). Moving up/down/left/right, return the fewest steps from the top-left to the bottom-right cell, or `-1` if impossible. Start and end count as open if they are `0`.

**Example**

```
[[0, 0, 0],
 [1, 1, 0],
 [0, 0, 0]]   ->  4
```
""",
            "function": "shortest_path",
            "starter": "def shortest_path(grid):\n    pass\n",
            "tests": [
                {"args": [[[0, 0, 0], [1, 1, 0], [0, 0, 0]]], "expected": 4},
                {"args": [[[0, 1], [1, 0]]], "expected": -1},
                {"args": [[[0]]], "expected": 0},
                {"args": [[[1, 0], [0, 0]]], "expected": -1},
                {"args": [[[0, 0, 1], [1, 0, 1], [1, 0, 0]]], "expected": 4},
            ],
            "hints": [
                "BFS from (0, 0), storing the distance with each cell.",
                "The first time you reach the bottom-right is the shortest path.",
            ],
            "solution": r'''from collections import deque


def shortest_path(grid):
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return dist
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if (0 <= nr < rows and 0 <= nc < cols
                    and grid[nr][nc] == 0 and (nr, nc) not in seen):
                seen.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    return -1
''',
        },
        {
            'id': 'rotting-oranges',
            'title': 'Rotting Oranges',
            'difficulty': 'Medium',
            "statement": """
In `grid`, `0` is empty, `1` a fresh orange and `2` a rotten one. Each minute, fresh oranges next to a rotten one (up/down/left/right) rot. Return the minutes until no fresh orange remains, or `-1` if that's impossible.

**Example**

```
[[2, 1, 1],
 [1, 1, 0],
 [0, 1, 1]]   ->  4
```
""",
            'function': 'oranges_rotting',
            'starter': 'def oranges_rotting(grid):\n    pass\n',
            'tests': [{'args': [[[2, 1, 1], [1, 1, 0], [0, 1, 1]]], 'expected': 4}, {'args': [[[2, 1, 1], [0, 1, 1], [1, 0, 1]]], 'expected': -1}, {'args': [[[0, 2]]], 'expected': 0}],
            'hints': ['Multi-source BFS: start with ALL rotten oranges in the queue.', 'Process the queue level by level; each level is one minute.'],
            'solution': r'''from collections import deque


def oranges_rotting(grid):
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue and fresh:
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return -1 if fresh else minutes
''',
        },
        {
            'id': 'word-ladder',
            'title': 'Word Ladder',
            'difficulty': 'Hard',
            "statement": """
Transform `begin` into `end` changing one letter at a time; every intermediate word must be in `words`. Return the number of words in the shortest sequence (including both ends), or `0` if impossible.

**Example**

```
ladder_length("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
->  5   (hit → hot → dot → dog → cog)
```
""",
            'function': 'ladder_length',
            'starter': 'def ladder_length(begin, end, words):\n    pass\n',
            'tests': [{'args': ['hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log', 'cog']], 'expected': 5}, {'args': ['hit', 'cog', ['hot', 'dot', 'dog', 'lot', 'log']], 'expected': 0}, {'args': ['a', 'c', ['a', 'b', 'c']], 'expected': 2}],
            'hints': ['Each word is a node; words one letter apart are neighbours. BFS finds the shortest path.', "Group words by patterns like 'h*t' to find neighbours quickly."],
            'solution': r'''from collections import defaultdict, deque


def ladder_length(begin, end, words):
    if end not in words:
        return 0
    patterns = defaultdict(list)
    for word in words:
        for i in range(len(word)):
            patterns[word[:i] + "*" + word[i + 1:]].append(word)

    queue = deque([(begin, 1)])
    seen = {begin}
    while queue:
        word, steps = queue.popleft()
        if word == end:
            return steps
        for i in range(len(word)):
            for nxt in patterns[word[:i] + "*" + word[i + 1:]]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, steps + 1))
    return 0
''',
        },
    ],
    "quiz": [
        {
            "question": "Which traversal finds the shortest path in an unweighted graph?",
            "options": ["DFS", "BFS", "In-order", "Binary search"],
            "answer": 1,
            "explanation": "BFS reaches nodes in order of distance from the start.",
        },
        {
            "question": "What is the time complexity of BFS with an adjacency list?",
            "options": ["O(V)", "O(E)", "O(V + E)", "O(V · E)"],
            "answer": 2,
            "explanation": "Every vertex is dequeued once and every edge is examined once (twice if undirected).",
        },
        {
            "question": "Why keep a `seen` set during graph traversal?",
            "options": [
                "To sort the output",
                "To avoid revisiting nodes and looping forever on cycles",
                "To save memory",
                "It's only needed for trees",
            ],
            "answer": 1,
            "explanation": "Unlike trees, graphs can contain cycles.",
        },
        {
            "question": "DFS is usually implemented with…",
            "options": ["A queue", "A stack or recursion", "A heap", "A hash map only"],
            "answer": 1,
            "explanation": "Last-in-first-out order dives deep before backtracking.",
        },
        {
            "question": "A topological sort is possible only if the directed graph…",
            "options": ["Is connected", "Has no cycles", "Is weighted", "Has an even number of nodes"],
            "answer": 1,
            "explanation": "A cycle means no node in it can come 'first'.",
        },
    ],
    "flashcards": [
        {'front': 'Most common way to store a graph in Python?', 'back': 'An adjacency list: dict mapping each node to a list of neighbours.'},
        {'front': 'BFS uses a ___ and finds ___?', 'back': 'A queue; shortest paths in unweighted graphs.'},
        {'front': 'DFS uses a ___?', 'back': 'A stack (or recursion), diving deep before backtracking.'},
        {'front': 'BFS/DFS time with an adjacency list?', 'back': 'O(V + E).'},
        {'front': 'Why mark nodes as seen when enqueuing?', 'back': 'To avoid adding the same node twice and looping forever on cycles.'},
    ],
}
