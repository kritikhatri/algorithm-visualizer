TOPIC = {
    "id": "heaps",
    "title": "Heaps & Priority Queues",
    "category": "Trees & Graphs",
    "summary": "Always grab the smallest (or largest) item fast with heapq.",
    "visualizer": "heap",
    "lesson": """
A **heap** is a complete binary tree where every parent is smaller than (or equal to) its children, a **min-heap**. The smallest element is always at the root, so you can read it in `O(1)` and remove it in `O(log n)`.

## Stored as a list

Because the tree is complete (filled level by level), it fits in a plain list with no pointers:

- children of index `i` are at `2i + 1` and `2i + 2`
- the parent of index `i` is at `(i - 1) // 2`

## Operations

- **Push**: append to the end, then **sift up**, swapping with the parent while smaller.
- **Pop**: take the root, move the last element to the root, then **sift down**, swapping with the smaller child while larger.
- **Heapify** a whole list in `O(n)`.

Watch both in the visualizer.

## Python's `heapq`

```python
import heapq
nums = [5, 1, 8, 3]
heapq.heapify(nums)        # O(n), nums is now a min-heap
heapq.heappush(nums, 2)
heapq.heappop(nums)        # 1
nums[0]                    # peek at the min
```

`heapq` only provides a **min-heap**. For a max-heap, push negated values (`-x`) and negate again when popping. To store items with priorities, push tuples: `(priority, item)`.

## When to reach for a heap

- **Top k / k-th largest**: keep a min-heap of size `k`. Each new item that beats the root replaces it. `O(n log k)`.
- **Merging k sorted lists**: the heap holds the current head of every list.
- **Scheduling, Dijkstra's shortest path, running median**.
""",
    "complexity": [
        {"operation": "Peek min (heap[0])", "time": "O(1)", "space": "O(1)"},
        {"operation": "heappush / heappop", "time": "O(log n)", "space": "O(1)"},
        {"operation": "heapify(list)", "time": "O(n)", "space": "O(1)"},
        {"operation": "Top-k with size-k heap", "time": "O(n log k)", "space": "O(k)"},
        {"operation": "Search for arbitrary value", "time": "O(n)", "space": "O(1)"},
    ],
    "snippets": [
        {
            "title": "A min-heap from scratch",
            "code": r'''class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, val):
        self.data.append(val)
        i = len(self.data) - 1
        while i > 0 and self.data[(i - 1) // 2] > self.data[i]:
            parent = (i - 1) // 2
            self.data[i], self.data[parent] = self.data[parent], self.data[i]
            i = parent

    def pop(self):
        data = self.data
        data[0], data[-1] = data[-1], data[0]
        smallest = data.pop()
        i = 0
        while True:
            left, right, best = 2 * i + 1, 2 * i + 2, i
            if left < len(data) and data[left] < data[best]:
                best = left
            if right < len(data) and data[right] < data[best]:
                best = right
            if best == i:
                return smallest
            data[i], data[best] = data[best], data[i]
            i = best


h = MinHeap()
for v in [5, 3, 8, 1]:
    h.push(v)
print([h.pop() for _ in range(4)])  # [1, 3, 5, 8]
''',
        },
        {
            "title": "Max-heap trick and priorities",
            "code": r'''import heapq

scores = [40, 95, 70, 88]
max_heap = [-s for s in scores]
heapq.heapify(max_heap)
print(-heapq.heappop(max_heap))   # 95

tasks = []
heapq.heappush(tasks, (2, "write tests"))
heapq.heappush(tasks, (1, "fix bug"))
print(heapq.heappop(tasks))       # (1, 'fix bug')
''',
        },
    ],
    "problems": [
        {
            "id": "kth-largest-element",
            "title": "Kth Largest Element",
            "difficulty": "Medium",
            "statement": """
Return the `k`-th largest element in `nums` (in sorted order, not the k-th distinct). Try to do better than sorting with a size-`k` heap.

**Example**

```
find_kth_largest([3, 2, 1, 5, 6, 4], 2)           ->  5
find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)  ->  4
```
""",
            "function": "find_kth_largest",
            "starter": "import heapq\n\n\ndef find_kth_largest(nums, k):\n    pass\n",
            "tests": [
                {"args": [[3, 2, 1, 5, 6, 4], 2], "expected": 5},
                {"args": [[3, 2, 3, 1, 2, 4, 5, 5, 6], 4], "expected": 4},
                {"args": [[1], 1], "expected": 1},
                {"args": [[7, 7, 7], 2], "expected": 7},
            ],
            "hints": [
                "Keep a min-heap of the k largest values seen so far.",
                "When it grows past k, pop the smallest. The root is the answer.",
            ],
            "solution": r'''import heapq


def find_kth_largest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
''',
        },
        {
            "id": "top-k-frequent",
            "title": "Top K Frequent Elements",
            "difficulty": "Medium",
            "statement": """
Return the `k` most frequent elements of `nums`, in any order. The answer is unique.

**Example**

```
top_k_frequent([1, 1, 1, 2, 2, 3], 2)  ->  [1, 2]
```
""",
            "function": "top_k_frequent",
            "compare": "unordered",
            "starter": "def top_k_frequent(nums, k):\n    pass\n",
            "tests": [
                {"args": [[1, 1, 1, 2, 2, 3], 2], "expected": [1, 2]},
                {"args": [[1], 1], "expected": [1]},
                {"args": [[4, 4, 5, 5, 5, 6], 1], "expected": [5]},
                {"args": [[-1, -1, 2, 2, 3], 2], "expected": [-1, 2]},
            ],
            "hints": [
                "Count with `collections.Counter`.",
                "`heapq.nlargest(k, counts, key=counts.get)` picks the top k keys.",
            ],
            "solution": r'''import heapq
from collections import Counter


def top_k_frequent(nums, k):
    counts = Counter(nums)
    return heapq.nlargest(k, counts, key=counts.get)
''',
        },
        {
            "id": "merge-k-sorted",
            "title": "Merge K Sorted Lists",
            "difficulty": "Hard",
            "statement": """
Given `lists`, a list of sorted Python lists, return one sorted list containing all their elements. Aim for `O(N log k)` where `N` is the total count.

**Example**

```
merge_k_sorted([[1, 4, 5], [1, 3, 4], [2, 6]])
->  [1, 1, 2, 3, 4, 4, 5, 6]
```
""",
            "function": "merge_k_sorted",
            "starter": "import heapq\n\n\ndef merge_k_sorted(lists):\n    pass\n",
            "tests": [
                {"args": [[[1, 4, 5], [1, 3, 4], [2, 6]]], "expected": [1, 1, 2, 3, 4, 4, 5, 6]},
                {"args": [[]], "expected": []},
                {"args": [[[], [1]]], "expected": [1]},
                {"args": [[[5], [1, 2], [3, 4]]], "expected": [1, 2, 3, 4, 5]},
            ],
            "hints": [
                "Push `(value, list_index, element_index)` for each list's first element.",
                "Pop the smallest, then push the next element from the same list.",
            ],
            "solution": r'''import heapq


def merge_k_sorted(lists):
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists) if lst]
    heapq.heapify(heap)
    merged = []
    while heap:
        value, i, j = heapq.heappop(heap)
        merged.append(value)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j + 1], i, j + 1))
    return merged
''',
        },
    ],
    "quiz": [
        {
            "question": "In a min-heap, where is the smallest element?",
            "options": ["The last index", "The root (index 0)", "Any leaf", "The middle"],
            "answer": 1,
            "explanation": "Every parent ≤ its children, so the root is the minimum.",
        },
        {
            "question": "What are the children of index i in a list-based heap?",
            "options": ["i + 1 and i + 2", "2i and 2i + 1", "2i + 1 and 2i + 2", "i // 2"],
            "answer": 2,
            "explanation": "With 0-based indexing, children are 2i + 1 and 2i + 2.",
        },
        {
            "question": "How do you get a max-heap with Python's heapq?",
            "options": [
                "heapq.maxheap()",
                "Push negated values",
                "Sort in reverse",
                "It's not possible",
            ],
            "answer": 1,
            "explanation": "The smallest negated value is the largest original value.",
        },
        {
            "question": "What is the cost of heapq.heappop on n items?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
            "answer": 1,
            "explanation": "The replacement root sifts down at most the tree's height.",
        },
        {
            "question": "To find the k largest of n numbers efficiently, keep…",
            "options": [
                "A max-heap of all n numbers",
                "A min-heap of size k",
                "A sorted list of size n",
                "A stack of size k",
            ],
            "answer": 1,
            "explanation": "The root is the smallest of the current top k; anything bigger replaces it. O(n log k).",
        },
    ],
}
