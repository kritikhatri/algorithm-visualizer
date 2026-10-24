TOPIC = {
    "id": "binary-search",
    "title": "Binary Search",
    "category": "Algorithms",
    "summary": "Halve the search space every step: O(log n) on sorted data.",
    "visualizer": "binary-search",
    "lesson": """
**Binary search** finds a target in a **sorted** list by repeatedly checking the middle element and throwing away the half that can't contain the answer.

With 1,000,000 items it needs at most about 20 checks, versus up to 1,000,000 for a linear scan.

## The template

```python
def binary_search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1      # target is in the right half
        else:
            hi = mid - 1      # target is in the left half
    return -1
```

## Getting the boundaries right

Off-by-one errors are the classic binary search bug. Pick one convention and stick to it:

- `lo <= hi` with `hi = len - 1` searches an **inclusive** range `[lo, hi]`.
- When the loop ends without finding the target, `lo` is the index where it **would be inserted**, which is handy for "search insert position".

## Binary search on the answer

Binary search works on anything **monotonic**, not just arrays. If you can answer "is `x` big enough?" with yes/no, and the answers go `no no no yes yes`, you can binary search for the first `yes`. Examples: minimum eating speed, smallest capacity to ship packages, square root.

## Python's `bisect` module

```python
import bisect
nums = [1, 3, 5, 7]
bisect.bisect_left(nums, 5)   # 2: first index where 5 could go
bisect.insort(nums, 4)        # inserts keeping order
```
""",
    "complexity": [
        {"operation": "Binary search", "time": "O(log n)", "space": "O(1)"},
        {"operation": "Linear search (for comparison)", "time": "O(n)", "space": "O(1)"},
        {"operation": "bisect.bisect_left", "time": "O(log n)", "space": "O(1)"},
        {"operation": "bisect.insort", "time": "O(n)*", "space": "O(1)"},
        {"operation": "Binary search on answer", "time": "O(log range × check)", "space": "O(1)"},
    ],
    "snippets": [
        {
            "title": "Lower bound (first index ≥ target)",
            "code": r'''def lower_bound(nums, target):
    lo, hi = 0, len(nums)       # half-open range [lo, hi)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


print(lower_bound([1, 2, 4, 4, 7], 4))  # 2
print(lower_bound([1, 2, 4, 4, 7], 5))  # 4
''',
        },
        {
            "title": "Binary search on the answer: integer square root",
            "code": r'''def int_sqrt(x):
    lo, hi = 0, x
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return hi


print(int_sqrt(17))  # 4
''',
        },
    ],
    "problems": [
        {
            "id": "binary-search",
            "title": "Binary Search",
            "difficulty": "Easy",
            "statement": """
Given a sorted list `nums` of distinct integers and a `target`, return its index or `-1` if it's absent. Must run in `O(log n)`.

**Example**

```
search([-1, 0, 3, 5, 9, 12], 9)  ->  4
search([-1, 0, 3, 5, 9, 12], 2)  ->  -1
```
""",
            "function": "search",
            "starter": "def search(nums, target):\n    pass\n",
            "tests": [
                {"args": [[-1, 0, 3, 5, 9, 12], 9], "expected": 4},
                {"args": [[-1, 0, 3, 5, 9, 12], 2], "expected": -1},
                {"args": [[5], 5], "expected": 0},
                {"args": [[], 1], "expected": -1},
                {"args": [[1, 3, 5, 7, 9, 11, 13], 1], "expected": 0},
            ],
            "hints": ["Compare with the middle; discard the half that can't contain the target."],
            "solution": r'''def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
''',
        },
        {
            "id": "search-insert-position",
            "title": "Search Insert Position",
            "difficulty": "Easy",
            "statement": """
Return the index of `target` in sorted `nums`, or the index where it would be inserted to keep the order.

**Example**

```
search_insert([1, 3, 5, 6], 5)  ->  2
search_insert([1, 3, 5, 6], 2)  ->  1
search_insert([1, 3, 5, 6], 7)  ->  4
```
""",
            "function": "search_insert",
            "starter": "def search_insert(nums, target):\n    pass\n",
            "tests": [
                {"args": [[1, 3, 5, 6], 5], "expected": 2},
                {"args": [[1, 3, 5, 6], 2], "expected": 1},
                {"args": [[1, 3, 5, 6], 7], "expected": 4},
                {"args": [[1, 3, 5, 6], 0], "expected": 0},
            ],
            "hints": ["Run normal binary search. If it fails, `lo` is the insertion point."],
            "solution": r'''def search_insert(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return lo
''',
        },
        {
            "id": "find-min-rotated",
            "title": "Minimum in Rotated Sorted Array",
            "difficulty": "Medium",
            "statement": """
A sorted list of distinct numbers was rotated at an unknown pivot (e.g. `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`). Return its minimum in `O(log n)`.

**Example**

```
find_min([3, 4, 5, 1, 2])  ->  1
find_min([11, 13, 15, 17]) ->  11
```
""",
            "function": "find_min",
            "starter": "def find_min(nums):\n    pass\n",
            "tests": [
                {"args": [[3, 4, 5, 1, 2]], "expected": 1},
                {"args": [[4, 5, 6, 7, 0, 1, 2]], "expected": 0},
                {"args": [[11, 13, 15, 17]], "expected": 11},
                {"args": [[2, 1]], "expected": 1},
                {"args": [[1]], "expected": 1},
            ],
            "hints": [
                "Compare `nums[mid]` with `nums[hi]`.",
                "If `nums[mid] > nums[hi]`, the minimum is to the right of mid; otherwise it's at mid or to the left.",
            ],
            "solution": r'''def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]
''',
        },
    ],
    "quiz": [
        {
            "question": "What must be true for binary search to work on a list?",
            "options": ["It has no duplicates", "It is sorted", "Its length is a power of 2", "It contains integers"],
            "answer": 1,
            "explanation": "Sorting is what lets you discard half the range after one comparison.",
        },
        {
            "question": "About how many comparisons does binary search need for 1,000,000 items?",
            "options": ["1,000", "500,000", "20", "1"],
            "answer": 2,
            "explanation": "log₂(1,000,000) ≈ 20.",
        },
        {
            "question": "nums[mid] < target. What's the next step (inclusive [lo, hi] version)?",
            "options": ["hi = mid - 1", "lo = mid + 1", "lo = mid", "return -1"],
            "answer": 1,
            "explanation": "Everything up to and including mid is too small.",
        },
        {
            "question": "When the standard loop ends without finding the target, what is lo?",
            "options": [
                "Always 0",
                "The index where target would be inserted",
                "The last index",
                "Undefined",
            ],
            "answer": 1,
            "explanation": "lo ends at the first position whose value is greater than target.",
        },
        {
            "question": "Which Python module provides binary search helpers?",
            "options": ["heapq", "bisect", "itertools", "functools"],
            "answer": 1,
            "explanation": "bisect_left, bisect_right and insort work on sorted lists.",
        },
    ],
}
