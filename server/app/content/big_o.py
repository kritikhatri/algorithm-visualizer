TOPIC = {
    "id": "big-o",
    "title": "Big-O & Complexity",
    "category": "Foundations",
    "summary": "Measure how running time and memory grow as input gets bigger.",
    "visualizer": "growth",
    "lesson": """
Big-O notation describes how the **work an algorithm does grows** as the input size `n` grows. It ignores constants and small terms because, for large inputs, the shape of the growth is what matters.

## Why it matters

Two correct solutions can behave very differently. A loop inside a loop over 100,000 items does about 10 billion steps, which takes far too long, while a single pass does 100,000 and finishes instantly. Interviewers and real systems care about this difference.

## Common classes (fastest to slowest)

| Class | Name | Typical example |
| --- | --- | --- |
| `O(1)` | Constant | Index into a list, dict lookup |
| `O(log n)` | Logarithmic | Binary search |
| `O(n)` | Linear | One loop over the input |
| `O(n log n)` | Linearithmic | Merge sort, `sorted()` |
| `O(n²)` | Quadratic | Nested loops over the input |
| `O(2ⁿ)` | Exponential | Trying every subset |

## Rules of thumb

- **Drop constants:** `O(2n)` is just `O(n)`.
- **Keep the biggest term:** `O(n² + n)` is `O(n²)`.
- **Sequential steps add, nested steps multiply.** Two separate loops are `O(n + n) = O(n)`; a loop inside a loop is `O(n · n) = O(n²)`.
- **Halving each step gives `log n`.** If the problem size is cut in half every iteration, there are about `log₂ n` iterations.

## Space complexity

Space complexity counts the **extra memory** an algorithm uses. Building a new list of size `n` is `O(n)` space; swapping values in place is `O(1)`. Recursion uses space too, because each call waits on the call stack.

## Python built-ins to know

`list.append` and `list.pop()` are `O(1)`, but `list.insert(0, x)` and `list.pop(0)` are `O(n)` because every element shifts. `x in list` is `O(n)`, while `x in set` and `x in dict` are `O(1)` on average.
""",
    "complexity": [
        {"operation": "list[i], list.append(x), list.pop()", "time": "O(1)", "space": "O(1)"},
        {"operation": "x in list, list.insert(0, x), list.pop(0)", "time": "O(n)", "space": "O(1)"},
        {"operation": "x in set / dict, d[key] = value", "time": "O(1) avg", "space": "O(1)"},
        {"operation": "sorted(list), list.sort()", "time": "O(n log n)", "space": "O(n)"},
        {"operation": "list slicing nums[a:b]", "time": "O(b − a)", "space": "O(b − a)"},
    ],
    "snippets": [
        {
            "title": "O(n²) vs O(n): checking for duplicates",
            "code": r'''def has_duplicate_slow(nums):
    # O(n²): compares every pair
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


def has_duplicate_fast(nums):
    # O(n) time, O(n) space: remember what we've seen
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


print(has_duplicate_slow([3, 1, 4, 1]))  # True
print(has_duplicate_fast([3, 1, 4, 5]))  # False
''',
        },
        {
            "title": "O(log n): halving the problem",
            "code": r'''def count_halvings(n):
    steps = 0
    while n > 1:
        n //= 2      # problem size halves every iteration
        steps += 1
    return steps


for n in (8, 1_000, 1_000_000):
    print(n, "->", count_halvings(n), "steps")
''',
        },
    ],
    "problems": [
        {
            "id": "sum-to-n",
            "title": "Sum 1 to n in O(1)",
            "difficulty": "Easy",
            "statement": """
Return the sum `1 + 2 + ... + n` **without a loop**, in constant time.

**Example**

```
sum_to_n(5)  ->  15
sum_to_n(0)  ->  0
```

*Constraints:* `0 <= n <= 10⁷`
""",
            "function": "sum_to_n",
            "starter": "def sum_to_n(n):\n    pass\n",
            "tests": [
                {"args": [5], "expected": 15},
                {"args": [0], "expected": 0},
                {"args": [1], "expected": 1},
                {"args": [100], "expected": 5050},
                {"args": [10000000], "expected": 50000005000000},
            ],
            "hints": [
                "Pair the first and last numbers: 1 + n, 2 + (n − 1), …",
                "There are n / 2 such pairs, each summing to n + 1.",
            ],
            "solution": r'''def sum_to_n(n):
    # Gauss's formula: O(1) time and space
    return n * (n + 1) // 2
''',
        },
        {
            "id": "running-sum",
            "title": "Running Sum",
            "difficulty": "Easy",
            "statement": """
Given a list `nums`, return a list where element `i` is the sum of `nums[0..i]`.

A naive solution re-adds every prefix (`O(n²)`). Do it in **one pass**, `O(n)`.

**Example**

```
running_sum([1, 2, 3, 4])  ->  [1, 3, 6, 10]
```
""",
            "function": "running_sum",
            "starter": "def running_sum(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4]], "expected": [1, 3, 6, 10]},
                {"args": [[1, 1, 1, 1, 1]], "expected": [1, 2, 3, 4, 5]},
                {"args": [[3, -1, 2]], "expected": [3, 2, 4]},
                {"args": [[]], "expected": []},
            ],
            "hints": ["Keep a variable holding the total so far and append it after each step."],
            "solution": r'''def running_sum(nums):
    result = []
    total = 0
    for num in nums:
        total += num
        result.append(total)
    return result
''',
        },
    ],
    "quiz": [
        {
            "question": "What is the time complexity of a loop over n items that contains another loop over n items?",
            "options": ["O(n)", "O(2n)", "O(n²)", "O(log n)"],
            "answer": 2,
            "explanation": "Nested loops multiply: n iterations × n iterations = n².",
        },
        {
            "question": "Simplify O(3n² + 5n + 100).",
            "options": ["O(3n²)", "O(n²)", "O(n² + n)", "O(n)"],
            "answer": 1,
            "explanation": "Drop constants and keep only the fastest-growing term.",
        },
        {
            "question": "Which Python operation is O(n) on a list?",
            "options": ["nums.append(x)", "nums[-1]", "nums.pop()", "nums.pop(0)"],
            "answer": 3,
            "explanation": "Removing from the front shifts every remaining element left. Use collections.deque for O(1) pops from the front.",
        },
        {
            "question": "An algorithm halves the input size on every step. What is its complexity?",
            "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
            "answer": 1,
            "explanation": "You can halve n only about log₂ n times before reaching 1.",
        },
        {
            "question": "What is the space complexity of reversing a list in place by swapping ends?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
            "answer": 0,
            "explanation": "Only a couple of index variables are used, regardless of n.",
        },
    ],
}
