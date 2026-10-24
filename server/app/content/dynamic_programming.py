TOPIC = {
    "id": "dynamic-programming",
    "title": "Dynamic Programming",
    "category": "Techniques",
    "summary": "Break problems into overlapping subproblems and reuse the answers.",
    "visualizer": "dp-table",
    "lesson": """
**Dynamic programming (DP)** solves a problem by combining answers to smaller subproblems, and **stores** each answer so it's never computed twice.

DP applies when a problem has:

1. **Optimal substructure**: the best answer is built from best answers to subproblems.
2. **Overlapping subproblems**: the same subproblems come up again and again.

## Two styles

**Top-down (memoization)**: write the natural recursion, then cache it.

```python
from functools import cache

@cache
def climb(n):
    if n <= 1:
        return 1
    return climb(n - 1) + climb(n - 2)
```

**Bottom-up (tabulation)**: fill a table from the smallest subproblem upward.

```python
def climb(n):
    dp = [1] * (n + 1)
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    return dp[n]
```

## A recipe for any DP problem

1. **Define the state**: what does `dp[i]` (or `dp[i][j]`) mean, in words?
2. **Find the recurrence**: how does `dp[i]` follow from smaller states?
3. **Set base cases**: the smallest states you know directly.
4. **Choose the order**: fill states so dependencies are ready first.
5. **Read the answer**: often `dp[n]` or `dp[m][n]`.

## 2D DP example: longest common subsequence

`dp[i][j]` = LCS length of the first `i` characters of `a` and the first `j` of `b`.

- If `a[i-1] == b[j-1]`: `dp[i][j] = dp[i-1][j-1] + 1`
- else: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

The visualizer fills this table cell by cell.

## Space optimization

If each row only depends on the previous row, keep just two rows (or two variables, like `a, b` for Fibonacci) to drop memory from `O(n·m)` to `O(m)`.
""",
    "complexity": [
        {"operation": "Climbing stairs / Fibonacci (1D)", "time": "O(n)", "space": "O(1) optimized"},
        {"operation": "House robber", "time": "O(n)", "space": "O(1) optimized"},
        {"operation": "Coin change (amount A, k coins)", "time": "O(A · k)", "space": "O(A)"},
        {"operation": "Longest common subsequence", "time": "O(n · m)", "space": "O(n · m)"},
        {"operation": "0/1 knapsack (n items, capacity W)", "time": "O(n · W)", "space": "O(W)"},
    ],
    "snippets": [
        {
            "title": "Coin change (fewest coins)",
            "code": r'''def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount       # dp[x] = fewest coins to make x
    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x:
                dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != INF else -1


print(coin_change([1, 2, 5], 11))  # 3  (5 + 5 + 1)
''',
        },
        {
            "title": "Longest common subsequence (2D table)",
            "code": r'''def lcs(a, b):
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[-1][-1]


print(lcs("abcde", "ace"))  # 3
''',
        },
    ],
    "problems": [
        {
            "id": "climbing-stairs",
            "title": "Climbing Stairs",
            "difficulty": "Easy",
            "statement": """
You can climb 1 or 2 steps at a time. In how many distinct ways can you reach step `n`?

**Example**

```
climb_stairs(2)  ->  2    (1+1, 2)
climb_stairs(3)  ->  3    (1+1+1, 1+2, 2+1)
```
""",
            "function": "climb_stairs",
            "starter": "def climb_stairs(n):\n    pass\n",
            "tests": [
                {"args": [1], "expected": 1},
                {"args": [2], "expected": 2},
                {"args": [3], "expected": 3},
                {"args": [5], "expected": 8},
                {"args": [45], "expected": 1836311903},
            ],
            "hints": [
                "To reach step n, your last move came from n − 1 or n − 2.",
                "ways(n) = ways(n − 1) + ways(n − 2).",
            ],
            "solution": r'''def climb_stairs(n):
    a, b = 1, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b
''',
        },
        {
            "id": "house-robber",
            "title": "House Robber",
            "difficulty": "Medium",
            "statement": """
Each house has some money; you can't rob two **adjacent** houses. Return the maximum you can rob.

**Example**

```
rob([1, 2, 3, 1])     ->  4    (1 + 3)
rob([2, 7, 9, 3, 1])  ->  12   (2 + 9 + 1)
```
""",
            "function": "rob",
            "starter": "def rob(nums):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 1]], "expected": 4},
                {"args": [[2, 7, 9, 3, 1]], "expected": 12},
                {"args": [[5]], "expected": 5},
                {"args": [[]], "expected": 0},
                {"args": [[2, 1, 1, 2]], "expected": 4},
            ],
            "hints": [
                "At each house: rob it (+ best from two houses back) or skip it (best from one house back).",
                "You only need the last two best values.",
            ],
            "solution": r'''def rob(nums):
    skip, take = 0, 0  # best totals ending before / at the previous house
    for money in nums:
        skip, take = max(skip, take), skip + money
    return max(skip, take)
''',
        },
        {
            "id": "coin-change",
            "title": "Coin Change",
            "difficulty": "Medium",
            "statement": """
Return the fewest coins (unlimited supply of each denomination in `coins`) needed to make `amount`, or `-1` if it can't be made.

**Example**

```
coin_change([1, 2, 5], 11)  ->  3
coin_change([2], 3)         ->  -1
```
""",
            "function": "coin_change",
            "starter": "def coin_change(coins, amount):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 5], 11], "expected": 3},
                {"args": [[2], 3], "expected": -1},
                {"args": [[1], 0], "expected": 0},
                {"args": [[1, 3, 4], 6], "expected": 2},
                {"args": [[186, 419, 83, 408], 6249], "expected": 20},
            ],
            "hints": [
                "Greedy (always the biggest coin) fails: try [1, 3, 4] with amount 6.",
                "dp[x] = min over coins c of dp[x − c] + 1.",
            ],
            "solution": r'''def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for x in range(1, amount + 1):
        for coin in coins:
            if coin <= x and dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
    return dp[amount] if dp[amount] != INF else -1
''',
        },
        {
            "id": "longest-common-subsequence",
            "title": "Longest Common Subsequence",
            "difficulty": "Medium",
            "statement": """
Return the length of the longest subsequence common to strings `a` and `b`. A subsequence keeps the order of characters but may skip some.

**Example**

```
longest_common_subsequence("abcde", "ace")  ->  3   ("ace")
longest_common_subsequence("abc", "def")    ->  0
```
""",
            "function": "longest_common_subsequence",
            "starter": "def longest_common_subsequence(a, b):\n    pass\n",
            "tests": [
                {"args": ["abcde", "ace"], "expected": 3},
                {"args": ["abc", "abc"], "expected": 3},
                {"args": ["abc", "def"], "expected": 0},
                {"args": ["AGGTAB", "GXTXAYB"], "expected": 4},
            ],
            "hints": [
                "Let dp[i][j] be the answer for a[:i] and b[:j].",
                "Matching last characters extend dp[i-1][j-1]; otherwise take the max of dropping one character.",
            ],
            "solution": r'''def longest_common_subsequence(a, b):
    prev = [0] * (len(b) + 1)
    for ch in a:
        curr = [0]
        for j, other in enumerate(b, start=1):
            curr.append(prev[j - 1] + 1 if ch == other else max(prev[j], curr[j - 1]))
        prev = curr
    return prev[-1]
''',
        },
    ],
    "quiz": [
        {
            "question": "Which two properties make a problem a good fit for DP?",
            "options": [
                "Sorted input and unique values",
                "Optimal substructure and overlapping subproblems",
                "Recursion and loops",
                "Graphs and trees",
            ],
            "answer": 1,
            "explanation": "Reusing stored answers only pays off if subproblems repeat and combine into the best answer.",
        },
        {
            "question": "What is memoization?",
            "options": [
                "Writing notes in comments",
                "Caching results of function calls to avoid recomputation",
                "Sorting before solving",
                "Using less memory",
            ],
            "answer": 1,
            "explanation": "Top-down DP = recursion + cache (e.g. @functools.cache).",
        },
        {
            "question": "Why does always picking the largest coin fail for coins [1, 3, 4], amount 6?",
            "options": [
                "It doesn't fail",
                "Greedy gives 4+1+1 (3 coins) but 3+3 uses 2",
                "4 is too big",
                "You can't reuse coins",
            ],
            "answer": 1,
            "explanation": "Locally best choices don't guarantee a globally best answer, which is why we use DP.",
        },
        {
            "question": "In bottom-up DP, why does fill order matter?",
            "options": [
                "It doesn't",
                "Each state must be computed after the states it depends on",
                "For readability",
                "To use less memory",
            ],
            "answer": 1,
            "explanation": "dp[i] reads dp[i-1] and dp[i-2], so those must already be filled.",
        },
        {
            "question": "LCS of strings of lengths n and m with a full table costs…",
            "options": ["O(n + m)", "O(n · m)", "O(2ⁿ)", "O(n log m)"],
            "answer": 1,
            "explanation": "One constant-time update per cell of an (n+1) × (m+1) table.",
        },
    ],
}
