TOPIC = {
    "id": "recursion",
    "title": "Recursion & Backtracking",
    "category": "Techniques",
    "summary": "Functions that call themselves, memoization, and exploring choices.",
    "visualizer": "recursion-tree",
    "lesson": """
A **recursive** function solves a problem by calling itself on a smaller version of the same problem.

Every recursive function needs:

1. **A base case**: a smallest input answered directly, which stops the recursion.
2. **A recursive case**: break the problem down and trust the function to solve the smaller pieces.

```python
def factorial(n):
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)   # recursive case
```

## The call stack

Each call waits for the ones it made to return. These waiting calls live on the **call stack**, so recursion uses `O(depth)` memory. Python limits depth to about 1000 by default, so very deep recursion raises `RecursionError`.

## Overlapping subproblems → memoization

Naive Fibonacci calls `fib(n-1)` and `fib(n-2)`, which recompute the same values over and over: `O(2ⁿ)` calls. Caching results (memoization) makes each value computed once, `O(n)`:

```python
from functools import cache

@cache
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

Open the visualizer to watch the call tree shrink when memoization is turned on.

## Backtracking

Backtracking explores choices one at a time: **choose → explore → un-choose**. It builds a partial answer, recurses, then undoes the last choice to try the next one. It's how you generate subsets, permutations, solve N-Queens or Sudoku.

```python
def backtrack(path, choices):
    if done(path):
        results.append(path[:])   # copy!
        return
    for choice in choices:
        path.append(choice)       # choose
        backtrack(path, ...)      # explore
        path.pop()                # un-choose
```
""",
    "complexity": [
        {"operation": "Naive Fibonacci", "time": "O(2ⁿ)", "space": "O(n)"},
        {"operation": "Memoized Fibonacci", "time": "O(n)", "space": "O(n)"},
        {"operation": "Generate all subsets", "time": "O(n · 2ⁿ)", "space": "O(n)"},
        {"operation": "Generate all permutations", "time": "O(n · n!)", "space": "O(n)"},
        {"operation": "Recursion depth d", "time": "—", "space": "O(d) stack"},
    ],
    "snippets": [
        {
            "title": "Memoization by hand",
            "code": r'''def fib(n, memo={}):
    if n < 2:
        return n
    if n not in memo:
        memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]


print(fib(50))  # 12586269025, instant
''',
        },
        {
            "title": "Backtracking: all subsets",
            "code": r'''def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])      # choose
            backtrack(i + 1, path)    # explore
            path.pop()                # un-choose

    backtrack(0, [])
    return result


print(subsets([1, 2, 3]))
''',
        },
    ],
    "problems": [
        {
            "id": "fibonacci",
            "title": "Fibonacci Number",
            "difficulty": "Easy",
            "statement": """
Return the `n`-th Fibonacci number, where `fib(0) = 0`, `fib(1) = 1`, and `fib(n) = fib(n-1) + fib(n-2)`.

The last test uses `n = 80`; naive recursion will time out, so memoize or iterate.

**Example**

```
fib(10)  ->  55
```
""",
            "function": "fib",
            "starter": "def fib(n):\n    pass\n",
            "tests": [
                {"args": [0], "expected": 0},
                {"args": [1], "expected": 1},
                {"args": [10], "expected": 55},
                {"args": [20], "expected": 6765},
                {"args": [80], "expected": 23416728348467685},
            ],
            "hints": ["Use `@functools.cache`, a dict memo, or just loop keeping the last two values."],
            "solution": r'''def fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
''',
        },
        {
            "id": "subsets",
            "title": "Subsets",
            "difficulty": "Medium",
            "statement": """
Return all possible subsets of `nums` (elements are unique). Any order is accepted, both for the subsets and inside each subset.

**Example**

```
subsets([1, 2, 3])
->  [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]
```
""",
            "function": "subsets",
            "compare": "unordered_nested",
            "starter": "def subsets(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3]],
                 "expected": [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]},
                {"args": [[0]], "expected": [[], [0]]},
                {"args": [[]], "expected": [[]]},
            ],
            "hints": [
                "Each element is either in or out: 2ⁿ subsets.",
                "Backtrack with a `start` index so you never reuse earlier elements.",
            ],
            "solution": r'''def subsets(nums):
    result = []

    def backtrack(start, path):
        result.append(path[:])
        for i in range(start, len(nums)):
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return result
''',
        },
        {
            "id": "permutations",
            "title": "Permutations",
            "difficulty": "Medium",
            "statement": """
Return all orderings of the distinct integers in `nums`. The list of permutations may be in any order.

**Example**

```
permute([1, 2, 3])
->  [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
```
""",
            "function": "permute",
            "compare": "unordered",
            "starter": "def permute(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3]],
                 "expected": [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]},
                {"args": [[0, 1]], "expected": [[0, 1], [1, 0]]},
                {"args": [[7]], "expected": [[7]]},
            ],
            "hints": [
                "Build a path; at each level try every number not already used.",
                "When the path has len(nums) items, record a copy.",
            ],
            "solution": r'''def permute(nums):
    result = []
    used = [False] * len(nums)

    def backtrack(path):
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, num in enumerate(nums):
            if not used[i]:
                used[i] = True
                path.append(num)
                backtrack(path)
                path.pop()
                used[i] = False

    backtrack([])
    return result
''',
        },
    ],
    "quiz": [
        {
            "question": "What happens if a recursive function has no base case?",
            "options": [
                "It returns None",
                "It recurses until Python raises RecursionError",
                "It runs once",
                "Python adds one automatically",
            ],
            "answer": 1,
            "explanation": "Without a stopping condition the call stack grows until the limit is hit.",
        },
        {
            "question": "Why is naive recursive Fibonacci slow?",
            "options": [
                "Python recursion is slow",
                "It recomputes the same subproblems exponentially many times",
                "Addition is expensive",
                "It uses too much memory",
            ],
            "answer": 1,
            "explanation": "fib(n-2) is computed by both fib(n) and fib(n-1), and so on down the tree.",
        },
        {
            "question": "What is the space complexity of recursion that goes d calls deep?",
            "options": ["O(1)", "O(d)", "O(2^d)", "O(log d)"],
            "answer": 1,
            "explanation": "Each pending call holds a frame on the call stack.",
        },
        {
            "question": "In backtracking, why call path.pop() after the recursive call?",
            "options": [
                "To free memory",
                "To undo the choice so the next option can be tried",
                "To return the answer",
                "It's optional",
            ],
            "answer": 1,
            "explanation": "Choose → explore → un-choose keeps one shared path correct for every branch.",
        },
        {
            "question": "How many subsets does a set of n elements have?",
            "options": ["n", "n²", "2ⁿ", "n!"],
            "answer": 2,
            "explanation": "Each element is independently in or out: 2 × 2 × … × 2.",
        },
    ],
}
