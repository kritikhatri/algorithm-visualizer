TOPIC = {
    "id": "greedy",
    "title": "Greedy Algorithms",
    "category": "Techniques",
    "summary": "Make the best local choice at each step, when that's provably enough.",
    "visualizer": "intervals",
    "lesson": """
A **greedy algorithm** builds an answer step by step, always taking the choice that looks best *right now*, and never reconsidering it. When it works, it's usually simple and fast, often just a sort plus one pass.

## The catch: greedy isn't always right

Making change for `6` with coins `[1, 3, 4]`: greedy takes `4`, then `1`, `1` (3 coins), but `3 + 3` uses only 2. Greedy is correct only when you can argue that the local choice never hurts. Otherwise, use dynamic programming.

## How to convince yourself a greedy works

- **Exchange argument:** take any optimal solution that differs from the greedy one, swap in the greedy choice, and show it doesn't get worse.
- **Stays ahead:** show that after each step the greedy solution is at least as good as any other partial solution.

## Classic greedy patterns

**Interval scheduling.** To fit the most non-overlapping meetings in one room, sort by **end time** and keep each meeting that starts after the last kept one ends. Finishing earliest leaves the most room for the rest. The visualizer animates this.

```python
def max_meetings(intervals):
    count, end = 0, float("-inf")
    for start, finish in sorted(intervals, key=lambda iv: iv[1]):
        if start >= end:
            count += 1
            end = finish
    return count
```

**Track the best so far.** Best time to buy and sell a stock: remember the cheapest price seen, and check today's profit against it.

**Reachability.** Jump Game: keep the furthest index reachable; if you ever stand beyond it, you're stuck.

**Sort by a smart key.** Many greedy solutions start with `sorted(..., key=...)`: by end time, by ratio, by deadline.
""",
    "complexity": [
        {"operation": "Interval scheduling (sort + scan)", "time": "O(n log n)", "space": "O(1)"},
        {"operation": "Single-pass greedy (stock, jump game)", "time": "O(n)", "space": "O(1)"},
        {"operation": "Huffman coding (with heap)", "time": "O(n log n)", "space": "O(n)"},
    ],
    "snippets": [
        {
            "title": "Greedy coin change: works for some coin sets, not others",
            "code": r'''def greedy_coins(coins, amount):
    used = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            amount -= coin
            used.append(coin)
    return used if amount == 0 else None


print(greedy_coins([1, 5, 10, 25], 63))  # [25, 25, 10, 1, 1, 1], optimal
print(greedy_coins([1, 3, 4], 6))        # [4, 1, 1], but 3 + 3 is better!
''',
        },
        {
            "title": "Fractional knapsack: take the best value per kg first",
            "code": r'''def fractional_knapsack(items, capacity):
    total = 0.0
    for value, weight in sorted(items, key=lambda it: it[0] / it[1], reverse=True):
        take = min(weight, capacity)
        total += value * take / weight
        capacity -= take
        if capacity == 0:
            break
    return total


print(fractional_knapsack([(60, 10), (100, 20), (120, 30)], 50))  # 240.0
''',
        },
    ],
    "problems": [
        {
            "id": "best-time-to-buy-sell-stock",
            "title": "Best Time to Buy and Sell Stock",
            "difficulty": "Easy",
            "statement": """
`prices[i]` is a stock's price on day `i`. Buy on one day and sell on a later day. Return the maximum profit, or `0` if no profit is possible.

**Example**

```
max_profit([7, 1, 5, 3, 6, 4])  ->  5   (buy at 1, sell at 6)
```
""",
            "function": "max_profit",
            "starter": "def max_profit(prices):\n    pass\n",
            "tests": [
                {"args": [[7, 1, 5, 3, 6, 4]], "expected": 5},
                {"args": [[7, 6, 4, 3, 1]], "expected": 0},
                {"args": [[2, 4, 1]], "expected": 2},
                {"args": [[3]], "expected": 0},
            ],
            "hints": ["Track the lowest price so far; each day, check the profit of selling today."],
            "solution": r'''def max_profit(prices):
    lowest = float("inf")
    best = 0
    for price in prices:
        lowest = min(lowest, price)
        best = max(best, price - lowest)
    return best
''',
        },
        {
            "id": "jump-game",
            "title": "Jump Game",
            "difficulty": "Medium",
            "statement": """
You start at index 0. `nums[i]` is the maximum jump length from index `i`. Return `True` if you can reach the last index.

**Example**

```
can_jump([2, 3, 1, 1, 4])  ->  True
can_jump([3, 2, 1, 0, 4])  ->  False
```
""",
            "function": "can_jump",
            "starter": "def can_jump(nums):\n    pass\n",
            "tests": [
                {"args": [[2, 3, 1, 1, 4]], "expected": True},
                {"args": [[3, 2, 1, 0, 4]], "expected": False},
                {"args": [[0]], "expected": True},
                {"args": [[1, 0, 1]], "expected": False},
            ],
            "hints": ["Keep the furthest index you can reach. If i ever exceeds it, you're stuck."],
            "solution": r'''def can_jump(nums):
    furthest = 0
    for i, jump in enumerate(nums):
        if i > furthest:
            return False
        furthest = max(furthest, i + jump)
    return True
''',
        },
        {
            "id": "non-overlapping-intervals",
            "title": "Non-overlapping Intervals",
            "difficulty": "Medium",
            "statement": """
Return the minimum number of intervals to remove so the rest don't overlap. Intervals that only touch (`[1, 2]` and `[2, 3]`) don't overlap.

**Example**

```
erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]])  ->  1
```
""",
            "function": "erase_overlap_intervals",
            "starter": "def erase_overlap_intervals(intervals):\n    pass\n",
            "tests": [
                {"args": [[[1, 2], [2, 3], [3, 4], [1, 3]]], "expected": 1},
                {"args": [[[1, 2], [1, 2], [1, 2]]], "expected": 2},
                {"args": [[[1, 2], [2, 3]]], "expected": 0},
                {"args": [[[0, 5], [1, 2], [3, 4], [5, 6]]], "expected": 1},
            ],
            "hints": [
                "Keeping the most intervals = removing the fewest.",
                "Sort by end time; keep an interval if it starts at or after the last kept end.",
            ],
            "solution": r'''def erase_overlap_intervals(intervals):
    kept, end = 0, float("-inf")
    for start, finish in sorted(intervals, key=lambda iv: iv[1]):
        if start >= end:
            kept += 1
            end = finish
    return len(intervals) - kept
''',
        },
    ],
    "quiz": [
        {
            "question": "What defines a greedy algorithm?",
            "options": [
                "It tries every possibility",
                "It takes the locally best choice at each step and never undoes it",
                "It always uses recursion",
                "It stores all subproblem answers",
            ],
            "answer": 1,
            "explanation": "That commitment is what makes greedy fast, and also what makes it risky.",
        },
        {
            "question": "To schedule the most non-overlapping meetings, sort by…",
            "options": ["Start time", "Duration", "End time", "Name"],
            "answer": 2,
            "explanation": "Finishing earliest leaves the most time for the remaining meetings.",
        },
        {
            "question": "Coins [1, 3, 4], amount 6: what does greedy (largest first) produce?",
            "options": ["3 + 3", "4 + 1 + 1", "1 × 6", "No answer"],
            "answer": 1,
            "explanation": "That's 3 coins, while the optimum is 2, so greedy fails for this coin set.",
        },
        {
            "question": "Which technique PROVES a greedy choice is safe?",
            "options": ["Memoization", "Exchange argument", "Binary search", "Recursion depth"],
            "answer": 1,
            "explanation": "Show you can swap the greedy choice into any optimal solution without making it worse.",
        },
        {
            "question": "If greedy can't be proven correct, what's the usual fallback?",
            "options": ["Sort differently", "Dynamic programming", "Use a stack", "Random guessing"],
            "answer": 1,
            "explanation": "DP considers all choices for each subproblem, at a higher cost.",
        },
    ],
    "flashcards": [
        {"front": "What is a greedy algorithm?", "back": "Take the locally best choice at each step and never revisit it."},
        {"front": "Interval scheduling: sort by what?", "back": "End time. Keep an interval if it starts at/after the last kept end."},
        {"front": "Name a case where greedy fails.", "back": "Coins [1, 3, 4] for 6: greedy gives 4+1+1, optimal is 3+3."},
        {"front": "Two ways to prove a greedy algorithm?", "back": "Exchange argument; 'greedy stays ahead'."},
        {"front": "Jump Game greedy idea?", "back": "Track the furthest reachable index; fail if the current index ever exceeds it."},
    ],
}
