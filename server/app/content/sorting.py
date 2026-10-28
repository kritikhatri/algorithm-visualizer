TOPIC = {
    "id": "sorting",
    "title": "Sorting Algorithms",
    "category": "Algorithms",
    "summary": "Bubble, selection, insertion, merge and quick sort, step by step.",
    "visualizer": "sorting",
    "lesson": """
Sorting puts items in order. It's rarely the whole problem, but it's often the **first step** that makes the rest easy: once data is sorted you can binary search it, merge it, or scan it with two pointers.

In real Python code, use `sorted(items)` or `items.sort()`. They use **Timsort**, which is `O(n log n)` and stable. Learning the classic algorithms teaches you the ideas behind them.

## The simple `O(n²)` sorts

- **Bubble sort** repeatedly swaps adjacent items that are out of order. After each pass the largest remaining item has "bubbled" to the end.
- **Selection sort** finds the minimum of the unsorted part and swaps it into place.
- **Insertion sort** grows a sorted prefix, inserting each new item where it belongs. It is fast on nearly-sorted data (`O(n)` best case).

## The `O(n log n)` sorts

- **Merge sort** (*divide and conquer*): split the list in half, sort each half recursively, then merge the two sorted halves. Always `O(n log n)`, stable, but needs `O(n)` extra space.
- **Quick sort**: choose a *pivot*, partition items into "less than pivot" and "greater than pivot", then sort each side. `O(n log n)` on average, `O(n²)` if pivots are consistently bad, and in place.

## Stability

A sort is **stable** if equal items keep their original relative order. This matters when sorting records by one field after another, e.g. sort by name, then stably by grade.

## Custom sort keys in Python

```python
people = [("Ana", 31), ("Bo", 25), ("Cy", 31)]
sorted(people, key=lambda p: p[1])           # by age
sorted(people, key=lambda p: (-p[1], p[0]))  # age desc, then name
```
""",
    "complexity": [
        {"operation": "Bubble sort", "time": "O(n²)", "space": "O(1)"},
        {"operation": "Selection sort", "time": "O(n²)", "space": "O(1)"},
        {"operation": "Insertion sort", "time": "O(n²), O(n) best", "space": "O(1)"},
        {"operation": "Merge sort", "time": "O(n log n)", "space": "O(n)"},
        {"operation": "Quick sort", "time": "O(n log n) avg, O(n²) worst", "space": "O(log n)"},
        {"operation": "Python sorted() (Timsort)", "time": "O(n log n)", "space": "O(n)"},
    ],
    "snippets": [
        {
            "title": "Merge sort",
            "code": r'''def merge_sort(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])

    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
''',
        },
        {
            "title": "Quick sort (Lomuto partition, in place)",
            "code": r'''def quick_sort(nums, low=0, high=None):
    if high is None:
        high = len(nums) - 1
    if low < high:
        p = partition(nums, low, high)
        quick_sort(nums, low, p - 1)
        quick_sort(nums, p + 1, high)
    return nums


def partition(nums, low, high):
    pivot = nums[high]
    i = low
    for j in range(low, high):
        if nums[j] < pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[high] = nums[high], nums[i]
    return i


print(quick_sort([10, 7, 8, 9, 1, 5]))
''',
        },
    ],
    "problems": [
        {
            "id": "implement-merge-sort",
            "title": "Implement Merge Sort",
            "difficulty": "Medium",
            "statement": """
Return a new list with the numbers of `nums` sorted ascending, **without** using `sorted()` or `.sort()`. Implement merge sort.

**Example**

```
merge_sort([5, 2, 4, 6, 1, 3])  ->  [1, 2, 3, 4, 5, 6]
```
""",
            "function": "merge_sort",
            "starter": "def merge_sort(nums):\n    pass\n",
            "tests": [
                {"args": [[5, 2, 4, 6, 1, 3]], "expected": [1, 2, 3, 4, 5, 6]},
                {"args": [[]], "expected": []},
                {"args": [[1]], "expected": [1]},
                {"args": [[3, -1, 3, 0, -1]], "expected": [-1, -1, 0, 3, 3]},
                {"args": [[9, 8, 7, 6, 5, 4, 3, 2, 1]], "expected": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            ],
            "hints": [
                "Base case: a list of length 0 or 1 is already sorted.",
                "Merge two sorted lists with two indices, always taking the smaller head.",
            ],
            "solution": r'''def merge_sort(nums):
    if len(nums) <= 1:
        return list(nums)
    mid = len(nums) // 2
    left, right = merge_sort(nums[:mid]), merge_sort(nums[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    return merged + left[i:] + right[j:]
''',
        },
        {
            "id": "sort-colors",
            "title": "Sort Colors",
            "difficulty": "Medium",
            "statement": """
`nums` contains only `0`, `1` and `2`. Sort it **in place** in one pass, without a library sort (the Dutch national flag problem).

**Example**

```
nums = [2, 0, 2, 1, 1, 0]
sort_colors(nums)
nums  ->  [0, 0, 1, 1, 2, 2]
```
""",
            "function": "sort_colors",
            "inplace": 0,
            "starter": "def sort_colors(nums):\n    pass\n",
            "tests": [
                {"args": [[2, 0, 2, 1, 1, 0]], "expected": [0, 0, 1, 1, 2, 2]},
                {"args": [[2, 0, 1]], "expected": [0, 1, 2]},
                {"args": [[0]], "expected": [0]},
                {"args": [[1, 1, 1]], "expected": [1, 1, 1]},
            ],
            "hints": [
                "Keep three pointers: `low` (next 0 slot), `mid` (current), `high` (next 2 slot).",
                "Swap 0s to low, 2s to high; when you swap with high, don't advance mid.",
            ],
            "solution": r'''def sort_colors(nums):
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
        else:
            mid += 1
''',
        },
        {
            "id": "merge-intervals",
            "title": "Merge Intervals",
            "difficulty": "Medium",
            "statement": """
Given a list of intervals `[start, end]`, merge all overlapping intervals and return them sorted by start.

**Example**

```
merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
->  [[1, 6], [8, 10], [15, 18]]
```
""",
            "function": "merge_intervals",
            "starter": "def merge_intervals(intervals):\n    pass\n",
            "tests": [
                {"args": [[[1, 3], [2, 6], [8, 10], [15, 18]]], "expected": [[1, 6], [8, 10], [15, 18]]},
                {"args": [[[1, 4], [4, 5]]], "expected": [[1, 5]]},
                {"args": [[[4, 7], [1, 4]]], "expected": [[1, 7]]},
                {"args": [[[1, 10], [2, 3], [4, 5]]], "expected": [[1, 10]]},
            ],
            "hints": [
                "Sort by start time first.",
                "If an interval starts before the last merged one ends, extend the last one's end.",
            ],
            "solution": r'''def merge_intervals(intervals):
    merged = []
    for start, end in sorted(intervals):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged
''',
        },
        {
            'id': 'largest-number',
            'title': 'Largest Number',
            'difficulty': 'Medium',
            "statement": """
Arrange non-negative integers `nums` to form the largest possible number, returned as a **string**.

**Example**

```
largest_number([3, 30, 34, 5, 9])  ->  "9534330"
```
""",
            'function': 'largest_number',
            'starter': 'def largest_number(nums):\n    pass\n',
            'tests': [{'args': [[10, 2]], 'expected': '210'}, {'args': [[3, 30, 34, 5, 9]], 'expected': '9534330'}, {'args': [[0, 0]], 'expected': '0'}, {'args': [[1]], 'expected': '1'}],
            'hints': ['Compare two numbers a, b as strings: which of a + b or b + a is bigger?', 'Use functools.cmp_to_key with that comparison. Watch out for all zeros.'],
            'solution': r'''from functools import cmp_to_key


def largest_number(nums):
    words = [str(n) for n in nums]
    words.sort(key=cmp_to_key(lambda a, b: (b + a > a + b) - (b + a < a + b)))
    result = "".join(words)
    return "0" if result[0] == "0" else result
''',
        },
        {
            'id': 'count-inversions',
            'title': 'Count Inversions',
            'difficulty': 'Hard',
            "statement": """
An inversion is a pair `i < j` with `nums[i] > nums[j]`. Count them in `O(n log n)` by adapting merge sort.

**Example**

```
count_inversions([2, 4, 1, 3, 5])  ->  3   ((2,1), (4,1), (4,3))
```
""",
            'function': 'count_inversions',
            'starter': 'def count_inversions(nums):\n    pass\n',
            'tests': [{'args': [[2, 4, 1, 3, 5]], 'expected': 3}, {'args': [[1, 2, 3]], 'expected': 0}, {'args': [[3, 2, 1]], 'expected': 3}, {'args': [[8, 4, 2, 1]], 'expected': 6}, {'args': [[]], 'expected': 0}],
            'hints': ["While merging, if you take from the right half, it's smaller than everything left in the left half.", 'Add len(left) − i to the count each time that happens.'],
            'solution': r'''def count_inversions(nums):
    def sort(values):
        if len(values) <= 1:
            return values, 0
        mid = len(values) // 2
        left, a = sort(values[:mid])
        right, b = sort(values[mid:])
        merged, i, j, count = [], 0, 0, a + b
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                count += len(left) - i
        merged += left[i:] + right[j:]
        return merged, count

    return sort(nums)[1]
''',
        },
    ],
    "quiz": [
        {
            "question": "Which sort is always O(n log n) and stable?",
            "options": ["Quick sort", "Merge sort", "Selection sort", "Bubble sort"],
            "answer": 1,
            "explanation": "Merge sort's split-and-merge is n log n in every case and preserves equal-element order.",
        },
        {
            "question": "When does insertion sort run in O(n)?",
            "options": [
                "On random data",
                "On reverse-sorted data",
                "On already (nearly) sorted data",
                "Never",
            ],
            "answer": 2,
            "explanation": "Each new element is already in place, so there's no shifting.",
        },
        {
            "question": "What causes quick sort's O(n²) worst case?",
            "options": [
                "Too many duplicates only",
                "Pivots that split the data very unevenly (e.g. always the min)",
                "Using recursion",
                "Small arrays",
            ],
            "answer": 1,
            "explanation": "With a bad pivot, each partition only removes one element.",
        },
        {
            "question": "What algorithm does Python's sorted() use?",
            "options": ["Quick sort", "Heap sort", "Timsort", "Bubble sort"],
            "answer": 2,
            "explanation": "Timsort is a hybrid of merge sort and insertion sort, optimized for real-world data.",
        },
        {
            "question": "What does it mean for a sort to be stable?",
            "options": [
                "It never crashes",
                "Equal elements keep their original relative order",
                "It uses O(1) space",
                "It is always O(n log n)",
            ],
            "answer": 1,
            "explanation": "Important when sorting by several keys one after another.",
        },
    ],
    "flashcards": [
        {'front': 'Which simple sort is fast on nearly-sorted data?', 'back': 'Insertion sort: O(n) best case.'},
        {'front': 'Merge sort time and space?', 'back': 'O(n log n) always; O(n) extra space; stable.'},
        {'front': "Quick sort's worst case and why?", 'back': 'O(n²) when pivots split very unevenly (e.g. always the min or max).'},
        {'front': "What does 'stable' mean for a sort?", 'back': 'Equal elements keep their original relative order.'},
        {'front': "What does Python's sorted() use?", 'back': 'Timsort: O(n log n), stable, fast on partially sorted data.'},
    ],
}
