TOPIC = {
    "id": "sliding-window",
    "title": "Sliding Window",
    "category": "Techniques",
    "summary": "Grow and shrink a window over an array or string in one pass.",
    "visualizer": "sliding-window",
    "lesson": """
Many problems ask about a **contiguous** subarray or substring: the longest, the shortest, or one with some sum. Checking every window is `O(n²)` or worse. A **sliding window** keeps two indices, `left` and `right`, and moves them forward so each element enters and leaves the window at most once: `O(n)`.

## Fixed-size windows

For a window of exactly `k` items, add the new right element and remove the element that just fell off the left:

```python
window = sum(nums[:k])
best = window
for right in range(k, len(nums)):
    window += nums[right] - nums[right - k]
    best = max(best, window)
```

## Variable-size windows

The general template expands `right` every step, and shrinks from `left` while the window breaks a rule:

```python
left = 0
for right, item in enumerate(items):
    add(item)                      # grow
    while window_is_invalid():
        remove(items[left])        # shrink
        left += 1
    update_answer(right - left + 1)
```

- **Longest window** problems: update the answer after shrinking, when the window is valid.
- **Shortest window** problems: update the answer *inside* the shrinking loop, while the window is still valid.

## What lives inside the window?

Usually a running sum, a `dict`/`Counter` of character counts, or a `set` of what's in the window. Pick whatever lets you check validity in `O(1)`.

## When it doesn't apply

Sliding windows rely on a monotonic rule: growing the window can only make it "more invalid" (or more valid). With negative numbers and a target sum, that breaks; use prefix sums with a hash map instead.
""",
    "complexity": [
        {"operation": "Fixed-size window pass", "time": "O(n)", "space": "O(1)"},
        {"operation": "Variable window with counts", "time": "O(n)", "space": "O(alphabet)"},
        {"operation": "Brute force over all windows", "time": "O(n²)", "space": "O(1)"},
    ],
    "snippets": [
        {
            "title": "Longest substring without repeating characters",
            "code": r'''def longest_unique(s):
    seen = set()
    left = best = 0
    for right, ch in enumerate(s):
        while ch in seen:          # shrink until ch is unique again
            seen.remove(s[left])
            left += 1
        seen.add(ch)
        best = max(best, right - left + 1)
    return best


print(longest_unique("abcabcbb"))  # 3 ("abc")
''',
        },
        {
            "title": "Shortest subarray with sum ≥ target",
            "code": r'''def min_subarray_len(target, nums):
    left = total = 0
    best = float("inf")
    for right, num in enumerate(nums):
        total += num
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float("inf") else best


print(min_subarray_len(7, [2, 3, 1, 2, 4, 3]))  # 2 ([4, 3])
''',
        },
    ],
    "problems": [
        {
            "id": "max-sum-subarray-k",
            "title": "Maximum Sum Subarray of Size K",
            "difficulty": "Easy",
            "statement": """
Return the largest sum of any `k` consecutive numbers in `nums` (`1 <= k <= len(nums)`).

**Example**

```
max_sum_k([2, 1, 5, 1, 3, 2], 3)  ->  9   ([5, 1, 3])
```
""",
            "function": "max_sum_k",
            "starter": "def max_sum_k(nums, k):\n    pass\n",
            "tests": [
                {"args": [[2, 1, 5, 1, 3, 2], 3], "expected": 9},
                {"args": [[2, 3, 4, 1, 5], 2], "expected": 7},
                {"args": [[-1, -2, -3], 1], "expected": -1},
                {"args": [[4], 1], "expected": 4},
            ],
            "hints": ["Sum the first k, then slide: add nums[right], subtract nums[right − k]."],
            "solution": r'''def max_sum_k(nums, k):
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        best = max(best, window)
    return best
''',
        },
        {
            "id": "longest-substring-no-repeat",
            "title": "Longest Substring Without Repeating Characters",
            "difficulty": "Medium",
            "statement": """
Return the length of the longest substring of `s` with no repeated characters.

**Example**

```
length_of_longest_substring("abcabcbb")  ->  3   ("abc")
length_of_longest_substring("pwwkew")    ->  3   ("wke")
```
""",
            "function": "length_of_longest_substring",
            "starter": "def length_of_longest_substring(s):\n    pass\n",
            "tests": [
                {"args": ["abcabcbb"], "expected": 3},
                {"args": ["bbbbb"], "expected": 1},
                {"args": ["pwwkew"], "expected": 3},
                {"args": [""], "expected": 0},
                {"args": ["abba"], "expected": 2},
            ],
            "hints": [
                "Keep a set of characters in the window.",
                "When a duplicate arrives, move left forward until the duplicate leaves.",
            ],
            "solution": r'''def length_of_longest_substring(s):
    last_seen = {}
    left = best = 0
    for right, ch in enumerate(s):
        if last_seen.get(ch, -1) >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best
''',
        },
        {
            "id": "minimum-window-substring",
            "title": "Minimum Window Substring",
            "difficulty": "Hard",
            "statement": """
Return the shortest substring of `s` that contains every character of `t` (including duplicates), or `""` if none exists. The answer is unique.

**Example**

```
min_window("ADOBECODEBANC", "ABC")  ->  "BANC"
```
""",
            "function": "min_window",
            "starter": "def min_window(s, t):\n    pass\n",
            "tests": [
                {"args": ["ADOBECODEBANC", "ABC"], "expected": "BANC"},
                {"args": ["a", "a"], "expected": "a"},
                {"args": ["a", "aa"], "expected": ""},
                {"args": ["aaflslflsldkalskaaa", "aaa"], "expected": "aaa"},
            ],
            "hints": [
                "Count what you need with a Counter of t, and track how many characters are still missing.",
                "Expand right until nothing is missing, then shrink left as far as possible, recording the best window.",
            ],
            "solution": r'''from collections import Counter


def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    left = 0
    best = (float("inf"), 0, 0)
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right + 1)
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return s[best[1]:best[2]] if best[0] != float("inf") else ""
''',
        },
    ],
    "quiz": [
        {
            "question": "Why is a sliding window O(n)?",
            "options": [
                "It only checks windows of size 1",
                "Each element enters and leaves the window at most once",
                "It uses binary search",
                "It sorts the input first",
            ],
            "answer": 1,
            "explanation": "left and right only move forward, so together they take at most 2n steps.",
        },
        {
            "question": "In a fixed-size window of k, how do you update the sum when sliding right?",
            "options": [
                "Recompute sum(nums[left:right])",
                "Add nums[right] and subtract nums[right − k]",
                "Multiply by k",
                "Add nums[right] only",
            ],
            "answer": 1,
            "explanation": "One element enters, one leaves: O(1) per step.",
        },
        {
            "question": "For 'shortest window' problems, when do you record the answer?",
            "options": [
                "Before expanding",
                "Inside the shrink loop, while the window is still valid",
                "Only at the very end",
                "Never; the window size is fixed",
            ],
            "answer": 1,
            "explanation": "Each valid window may be the shortest, so record it before shrinking further.",
        },
        {
            "question": "Which input breaks the basic 'sum ≥ target' sliding window?",
            "options": ["Sorted numbers", "Negative numbers", "Duplicates", "Very long arrays"],
            "answer": 1,
            "explanation": "With negatives, shrinking can increase the sum, so the monotonic rule fails. Use prefix sums.",
        },
        {
            "question": "What usually tracks the window's contents for string problems?",
            "options": ["A heap", "A Counter/dict of character counts", "A linked list", "Recursion"],
            "answer": 1,
            "explanation": "Counts let you add/remove characters and check validity in O(1).",
        },
    ],
    "flashcards": [
        {"front": "Sliding window time complexity, and why?", "back": "O(n): left and right only move forward, so each element enters and leaves once."},
        {"front": "Variable window template?", "back": "Expand right each step; while the window is invalid, remove items[left] and left += 1; then update the answer."},
        {"front": "Fixed window of size k: how to slide the sum?", "back": "window += nums[right] − nums[right − k]."},
        {"front": "Longest vs shortest window: where do you update the answer?", "back": "Longest: after shrinking (window valid). Shortest: inside the shrink loop."},
        {"front": "When does a sum-based sliding window fail?", "back": "With negative numbers; use prefix sums + a hash map instead."},
    ],
}
