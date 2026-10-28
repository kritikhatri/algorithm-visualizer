TOPIC = {
    "id": "arrays",
    "title": "Arrays & Two Pointers",
    "category": "Linear Structures",
    "summary": "Python lists, in-place tricks, and the two-pointer technique.",
    "visualizer": "two-pointers",
    "lesson": """
An **array** stores items next to each other in memory, so any element can be reached instantly by its index. In Python, the built-in `list` is a dynamic array: it grows automatically as you `append`.

## Key operations

- **Access** `nums[i]`: `O(1)`. The address is computed directly from the index.
- **Append / pop at the end**: `O(1)` amortized.
- **Insert / delete in the middle**: `O(n)`, because elements after the position must shift.
- **Search for a value**: `O(n)` unless the array is sorted.

## The two-pointer technique

Many array problems become linear when you move **two indices** through the data instead of checking every pair.

1. **Opposite ends**: start `left = 0`, `right = len(nums) - 1` and move them toward each other. Used for pair sums in sorted arrays, palindromes, and reversing.
2. **Same direction (fast/slow)**: a `slow` pointer marks where the next "kept" element goes while `fast` scans ahead. Used for removing duplicates or moving zeros in place.

## Example: pair sum in a sorted array

If `nums[left] + nums[right]` is too small, the only way to grow the sum is to move `left` right. If it's too big, move `right` left. Each step discards one candidate, so the whole search is `O(n)` instead of `O(n²)`.

## Python tips

- `nums[::-1]` makes a reversed copy (`O(n)` extra space); `nums.reverse()` reverses in place.
- Swap without a temp variable: `a, b = b, a`.
- `enumerate(nums)` gives index and value together.
""",
    "complexity": [
        {"operation": "Access nums[i]", "time": "O(1)", "space": "O(1)"},
        {"operation": "Append / pop at end", "time": "O(1)*", "space": "O(1)"},
        {"operation": "Insert / delete at index", "time": "O(n)", "space": "O(1)"},
        {"operation": "Linear search", "time": "O(n)", "space": "O(1)"},
        {"operation": "Two-pointer scan", "time": "O(n)", "space": "O(1)"},
    ],
    "snippets": [
        {
            "title": "Two pointers from opposite ends",
            "code": r'''def pair_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1      # need a bigger sum
        else:
            right -= 1     # need a smaller sum
    return []


print(pair_sum_sorted([1, 3, 4, 6, 8, 11], 10))  # [2, 3]
''',
        },
        {
            "title": "Fast and slow pointers (in place)",
            "code": r'''def remove_duplicates(nums):
    """Remove duplicates from a sorted list in place; return the new length."""
    if not nums:
        return 0
    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]
    return slow + 1


data = [1, 1, 2, 3, 3, 3, 4]
k = remove_duplicates(data)
print(data[:k])  # [1, 2, 3, 4]
''',
        },
    ],
    "problems": [
        {
            "id": "pair-sum-sorted",
            "title": "Pair Sum in Sorted Array",
            "difficulty": "Easy",
            "statement": """
Given a list `nums` sorted in ascending order and an integer `target`, return the indices `[i, j]` (`i < j`) of the two numbers that add up to `target`. Exactly one answer exists.

Use `O(1)` extra space.

**Example**

```
pair_sum_sorted([2, 7, 11, 15], 9)  ->  [0, 1]
```
""",
            "function": "pair_sum_sorted",
            "starter": "def pair_sum_sorted(nums, target):\n    pass\n",
            "tests": [
                {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                {"args": [[1, 3, 4, 6, 8, 11], 10], "expected": [2, 3]},
                {"args": [[-3, -1, 0, 2, 5], 4], "expected": [1, 4]},
                {"args": [[1, 2], 3], "expected": [0, 1]},
            ],
            "hints": [
                "Start one pointer at each end.",
                "If the sum is too small, move the left pointer right; if too big, move the right pointer left.",
            ],
            "solution": r'''def pair_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return [left, right]
        if total < target:
            left += 1
        else:
            right -= 1
    return []
''',
        },
        {
            "id": "valid-palindrome",
            "title": "Valid Palindrome",
            "difficulty": "Easy",
            "statement": """
Return `True` if string `s` reads the same forwards and backwards after **lowercasing** it and **ignoring non-alphanumeric characters**.

**Example**

```
is_palindrome("A man, a plan, a canal: Panama")  ->  True
is_palindrome("race a car")                       ->  False
```
""",
            "function": "is_palindrome",
            "starter": "def is_palindrome(s):\n    pass\n",
            "tests": [
                {"args": ["A man, a plan, a canal: Panama"], "expected": True},
                {"args": ["race a car"], "expected": False},
                {"args": [" "], "expected": True},
                {"args": ["No 'x' in Nixon"], "expected": True},
                {"args": ["ab"], "expected": False},
            ],
            "hints": [
                "Use two pointers moving inward.",
                "Skip characters where `ch.isalnum()` is False.",
            ],
            "solution": r'''def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if not s[left].isalnum():
            left += 1
        elif not s[right].isalnum():
            right -= 1
        elif s[left].lower() != s[right].lower():
            return False
        else:
            left += 1
            right -= 1
    return True
''',
        },
        {
            "id": "move-zeroes",
            "title": "Move Zeroes",
            "difficulty": "Easy",
            "statement": """
Move all `0`s in `nums` to the end **in place**, keeping the relative order of the other elements. Your function doesn't need to return anything; the test checks `nums` after the call.

**Example**

```
nums = [0, 1, 0, 3, 12]
move_zeroes(nums)
nums  ->  [1, 3, 12, 0, 0]
```
""",
            "function": "move_zeroes",
            "inplace": 0,
            "starter": "def move_zeroes(nums):\n    pass\n",
            "tests": [
                {"args": [[0, 1, 0, 3, 12]], "expected": [1, 3, 12, 0, 0]},
                {"args": [[0]], "expected": [0]},
                {"args": [[1, 2, 3]], "expected": [1, 2, 3]},
                {"args": [[0, 0, 1]], "expected": [1, 0, 0]},
            ],
            "hints": [
                "Keep a `slow` index for where the next non-zero belongs.",
                "Swap `nums[slow]` and `nums[fast]` whenever `nums[fast]` is non-zero.",
            ],
            "solution": r'''def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow], nums[fast] = nums[fast], nums[slow]
            slow += 1
''',
        },
        {
            'id': 'container-with-most-water',
            'title': 'Container With Most Water',
            'difficulty': 'Medium',
            "statement": """
`height[i]` is the height of a vertical line at position `i`. Pick two lines that, with the x-axis, hold the most water. Return that area: `min(height[i], height[j]) * (j - i)`.

**Example**

```
max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])  ->  49
```
""",
            'function': 'max_area',
            'starter': 'def max_area(height):\n    pass\n',
            'tests': [{'args': [[1, 8, 6, 2, 5, 4, 8, 3, 7]], 'expected': 49}, {'args': [[1, 1]], 'expected': 1}, {'args': [[4, 3, 2, 1, 4]], 'expected': 16}, {'args': [[1, 2, 1]], 'expected': 2}],
            'hints': ['Start with the widest container: pointers at both ends.', 'Always move the shorter line inward. Moving the taller one can never help.'],
            'solution': r'''def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        best = max(best, min(height[left], height[right]) * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best
''',
        },
        {
            'id': 'three-sum',
            'title': '3Sum',
            'difficulty': 'Medium',
            "statement": """
Return all **unique** triplets `[a, b, c]` from `nums` with `a + b + c == 0`. The order of triplets and of numbers inside them doesn't matter.

**Example**

```
three_sum([-1, 0, 1, 2, -1, -4])  ->  [[-1, -1, 2], [-1, 0, 1]]
```
""",
            'function': 'three_sum',
            'compare': 'unordered_nested',
            'starter': 'def three_sum(nums):\n    pass\n',
            'tests': [{'args': [[-1, 0, 1, 2, -1, -4]], 'expected': [[-1, -1, 2], [-1, 0, 1]]}, {'args': [[0, 1, 1]], 'expected': []}, {'args': [[0, 0, 0]], 'expected': [[0, 0, 0]]}, {'args': [[-2, 0, 1, 1, 2]], 'expected': [[-2, 0, 2], [-2, 1, 1]]}],
            'hints': ['Sort first. Fix one number, then find pairs with two pointers.', 'Skip equal neighbours to avoid duplicate triplets.'],
            'solution': r'''def three_sum(nums):
    nums = sorted(nums)
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
    return result
''',
        },
    ],
    "quiz": [
        {
            "question": "Why is accessing nums[i] O(1)?",
            "options": [
                "Python caches recent lookups",
                "The element's address is computed directly from i",
                "Lists are sorted",
                "It's actually O(log n)",
            ],
            "answer": 1,
            "explanation": "Elements are stored contiguously, so the address is start + i × size.",
        },
        {
            "question": "What is the cost of nums.insert(0, x) on a list of n items?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
            "answer": 2,
            "explanation": "Every existing element shifts one position right.",
        },
        {
            "question": "In a sorted array, the pair sum at (left, right) is smaller than the target. What do you do?",
            "options": ["Move right left", "Move left right", "Move both", "Restart from 0"],
            "answer": 1,
            "explanation": "Moving left rightward is the only way to increase the sum.",
        },
        {
            "question": "Which technique removes duplicates from a sorted list with O(1) extra space?",
            "options": ["Convert to a set", "Fast and slow pointers", "Sort again", "Recursion"],
            "answer": 1,
            "explanation": "slow marks the end of the unique prefix while fast scans ahead.",
        },
        {
            "question": "What does nums[::-1] return?",
            "options": [
                "Reverses nums in place",
                "A new reversed list",
                "The last element",
                "An error",
            ],
            "answer": 1,
            "explanation": "Slicing always creates a new list; use nums.reverse() to reverse in place.",
        },
    ],
    "flashcards": [
        {'front': 'Time to access nums[i] in a Python list?', 'back': 'O(1): the address is computed directly from the index.'},
        {'front': 'Time to insert at the front of a list?', 'back': 'O(n): every element shifts right. Use collections.deque for O(1).'},
        {'front': 'When does the opposite-ends two-pointer trick work?', 'back': 'When the data is sorted (or has a monotonic property), so each move safely discards candidates.'},
        {'front': 'What are fast/slow pointers in an array?', 'back': 'slow marks where the next kept element goes; fast scans ahead. Used for in-place filtering.'},
        {'front': 'nums[::-1] vs nums.reverse()?', 'back': 'Slicing makes a new reversed list (O(n) space); reverse() reverses in place.'},
    ],
}
