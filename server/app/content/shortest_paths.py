TOPIC = {
    "id": "shortest-paths",
    "title": "Shortest Paths: Dijkstra",
    "category": "Trees & Graphs",
    "summary": "Find the cheapest route through a weighted graph with a priority queue.",
    "visualizer": "dijkstra",
    "lesson": """
BFS finds shortest paths when every edge costs the same. When edges have different **weights** (distances, times, prices), you need **Dijkstra's algorithm**.

## The idea

Keep a tentative distance for every node, starting at `0` for the source and `∞` for everything else. Repeatedly:

1. Take the **unvisited node with the smallest distance**. A min-heap (`heapq`) does this in `O(log n)`.
2. Its distance is now final.
3. **Relax** each outgoing edge: if `dist[node] + weight < dist[neighbour]`, you've found a shorter route, so update it and push it onto the heap.

```python
import heapq

def dijkstra(graph, source):
    dist = {source: 0}
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue                     # stale entry
        for nxt, weight in graph[node]:
            nd = d + weight
            if nd < dist.get(nxt, float("inf")):
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist
```

Instead of a "decrease key" operation, Python code simply pushes a new entry and **skips stale ones** when they're popped.

## Why it works, and its one rule

Because every weight is **non-negative**, once a node is popped with the smallest distance, no later path can be shorter. With negative edges that guarantee breaks; use **Bellman-Ford** (relax every edge `V − 1` times, `O(V·E)`), which also detects negative cycles.

## Variations to recognize

- **Grid with costs** (minimum effort, minimum path sum with moves in any direction): nodes are cells.
- **At most k stops**: Bellman-Ford limited to `k + 1` rounds, or Dijkstra over `(node, stops)` states.
- **All pairs**: Floyd–Warshall, `O(V³)`, for small graphs.
""",
    "complexity": [
        {"operation": "Dijkstra with a binary heap", "time": "O((V + E) log V)", "space": "O(V + E)"},
        {"operation": "Bellman-Ford", "time": "O(V · E)", "space": "O(V)"},
        {"operation": "Floyd–Warshall (all pairs)", "time": "O(V³)", "space": "O(V²)"},
        {"operation": "BFS (all weights equal)", "time": "O(V + E)", "space": "O(V)"},
    ],
    "snippets": [
        {
            "title": "Dijkstra with path reconstruction",
            "code": r'''import heapq

graph = {
    "A": [("B", 4), ("C", 1)],
    "B": [("D", 1)],
    "C": [("B", 2), ("D", 5)],
    "D": [],
}

dist = {"A": 0}
parent = {"A": None}
heap = [(0, "A")]
while heap:
    d, node = heapq.heappop(heap)
    if d > dist[node]:
        continue
    for nxt, w in graph[node]:
        if d + w < dist.get(nxt, float("inf")):
            dist[nxt] = d + w
            parent[nxt] = node
            heapq.heappush(heap, (d + w, nxt))

path, node = [], "D"
while node:
    path.append(node)
    node = parent[node]
print(dist["D"], " -> ".join(reversed(path)))  # 4 A -> C -> B -> D
''',
        },
        {
            "title": "Bellman-Ford (handles negative edges)",
            "code": r'''def bellman_ford(n, edges, source):
    dist = [float("inf")] * n
    dist[source] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("negative cycle")
    return dist


print(bellman_ford(4, [(0, 1, 4), (0, 2, 5), (2, 1, -3), (1, 3, 2)], 0))
''',
        },
    ],
    "problems": [
        {
            "id": "network-delay-time",
            "title": "Network Delay Time",
            "difficulty": "Medium",
            "statement": """
`times[i] = [u, v, w]` means a signal travels from node `u` to node `v` in `w` time. Nodes are `1..n`. A signal starts at node `k`; return how long until **all** nodes receive it, or `-1` if some never do.

**Example**

```
network_delay_time([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2)  ->  2
```
""",
            "function": "network_delay_time",
            "starter": "import heapq\n\n\ndef network_delay_time(times, n, k):\n    pass\n",
            "tests": [
                {"args": [[[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2], "expected": 2},
                {"args": [[[1, 2, 1]], 2, 1], "expected": 1},
                {"args": [[[1, 2, 1]], 2, 2], "expected": -1},
                {"args": [[[1, 2, 4], [1, 3, 1], [3, 2, 1]], 3, 1], "expected": 2},
            ],
            "hints": [
                "Run Dijkstra from k.",
                "The answer is the largest shortest distance, if every node was reached.",
            ],
            "solution": r'''import heapq
from collections import defaultdict


def network_delay_time(times, n, k):
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {}
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        for nxt, w in graph[node]:
            if nxt not in dist:
                heapq.heappush(heap, (d + w, nxt))
    return max(dist.values()) if len(dist) == n else -1
''',
        },
        {
            "id": "path-with-minimum-effort",
            "title": "Path With Minimum Effort",
            "difficulty": "Medium",
            "statement": """
`heights` is a grid. Moving up/down/left/right between cells costs the absolute height difference. A route's **effort** is its largest single step. Return the minimum effort to go from the top-left to the bottom-right.

**Example**

```
[[1, 2, 2],
 [3, 8, 2],
 [5, 3, 5]]   ->  2
```
""",
            "function": "minimum_effort_path",
            "starter": "import heapq\n\n\ndef minimum_effort_path(heights):\n    pass\n",
            "tests": [
                {"args": [[[1, 2, 2], [3, 8, 2], [5, 3, 5]]], "expected": 2},
                {"args": [[[1, 2, 3], [3, 8, 4], [5, 3, 5]]], "expected": 1},
                {"args": [[[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]]], "expected": 0},
                {"args": [[[7]]], "expected": 0},
            ],
            "hints": [
                "Dijkstra, but a path's cost is the MAX step so far rather than the sum.",
                "Push (effort, r, c); the first time you pop the target, that's the answer.",
            ],
            "solution": r'''import heapq


def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    best = [[float("inf")] * cols for _ in range(rows)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        effort, r, c = heapq.heappop(heap)
        if (r, c) == (rows - 1, cols - 1):
            return effort
        if effort > best[r][c]:
            continue
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                step = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if step < best[nr][nc]:
                    best[nr][nc] = step
                    heapq.heappush(heap, (step, nr, nc))
''',
        },
        {
            "id": "cheapest-flights-k-stops",
            "title": "Cheapest Flights Within K Stops",
            "difficulty": "Hard",
            "statement": """
`flights[i] = [from, to, price]` among cities `0..n-1`. Return the cheapest price from `src` to `dst` using **at most `k` stops** (so at most `k + 1` flights), or `-1`.

**Example**

```
find_cheapest_price(4, [[0,1,100],[1,2,100],[2,0,100],[1,3,600],[2,3,200]], 0, 3, 1)  ->  700
```
""",
            "function": "find_cheapest_price",
            "starter": "def find_cheapest_price(n, flights, src, dst, k):\n    pass\n",
            "tests": [
                {"args": [4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1], "expected": 700},
                {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1], "expected": 200},
                {"args": [3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0], "expected": 500},
                {"args": [3, [[0, 1, 100]], 0, 2, 1], "expected": -1},
            ],
            "hints": [
                "Plain Dijkstra ignores the stop limit. Bellman-Ford naturally counts edges.",
                "Run k + 1 rounds; in each round relax every flight using a COPY of last round's prices.",
            ],
            "solution": r'''def find_cheapest_price(n, flights, src, dst, k):
    prices = [float("inf")] * n
    prices[src] = 0
    for _ in range(k + 1):
        updated = prices[:]
        for u, v, cost in flights:
            if prices[u] + cost < updated[v]:
                updated[v] = prices[u] + cost
        prices = updated
    return -1 if prices[dst] == float("inf") else prices[dst]
''',
        },
    ],
    "quiz": [
        {
            "question": "Which data structure does Dijkstra use to pick the next node?",
            "options": ["Stack", "Queue", "Min-heap / priority queue", "Hash set"],
            "answer": 2,
            "explanation": "It always expands the closest unfinished node, so it needs the minimum quickly.",
        },
        {
            "question": "Dijkstra fails when the graph has…",
            "options": ["Cycles", "Negative edge weights", "More than 100 nodes", "Undirected edges"],
            "answer": 1,
            "explanation": "A negative edge could make an already-finalized node cheaper. Use Bellman-Ford.",
        },
        {
            "question": "What does 'relaxing' an edge (u, v, w) mean?",
            "options": [
                "Removing it",
                "If dist[u] + w < dist[v], update dist[v]",
                "Setting its weight to 0",
                "Reversing its direction",
            ],
            "answer": 1,
            "explanation": "You check whether going through u gives v a shorter route.",
        },
        {
            "question": "Dijkstra's time complexity with a binary heap?",
            "options": ["O(V)", "O(V + E)", "O((V + E) log V)", "O(V³)"],
            "answer": 2,
            "explanation": "Each edge may push onto the heap, and heap operations cost log V.",
        },
        {
            "question": "If all edges have weight 1, what's simpler than Dijkstra?",
            "options": ["DFS", "BFS", "Binary search", "Sorting"],
            "answer": 1,
            "explanation": "BFS visits nodes in order of edge count, which equals distance here.",
        },
    ],
    "flashcards": [
        {"front": "Dijkstra in one sentence?", "back": "Repeatedly finalize the closest unvisited node (via a min-heap) and relax its edges."},
        {"front": "Dijkstra's key requirement?", "back": "Non-negative edge weights."},
        {"front": "How does Python Dijkstra handle 'decrease key'?", "back": "Push a new (dist, node) entry and skip stale entries when popped (if d > dist[node]: continue)."},
        {"front": "Bellman-Ford: what and when?", "back": "Relax all edges V − 1 times, O(V·E). Works with negative edges and detects negative cycles."},
        {"front": "Dijkstra time complexity?", "back": "O((V + E) log V) with a binary heap."},
    ],
}
