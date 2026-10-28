TOPIC = {
    "id": "bit-manipulation",
    "title": "Bit Manipulation",
    "category": "Foundations",
    "summary": "Work directly with binary: AND, OR, XOR, shifts and their tricks.",
    "visualizer": "bits",
    "lesson": """
Computers store integers in **binary**: each bit is a power of two. `13` is `1101` = 8 + 4 + 1. Bit manipulation operates on those bits directly, which makes some problems tiny and fast.

## The operators

| Operator | Python | Rule | Example (`12`, `10`) |
| --- | --- | --- | --- |
| AND | `a & b` | 1 if **both** bits are 1 | `1100 & 1010 = 1000` (8) |
| OR | `a \\| b` | 1 if **either** bit is 1 | `1100 \\| 1010 = 1110` (14) |
| XOR | `a ^ b` | 1 if the bits **differ** | `1100 ^ 1010 = 0110` (6) |
| NOT | `~a` | flips every bit | `~12 = -13` |
| Left shift | `a << k` | multiply by 2ᵏ | `3 << 2 = 12` |
| Right shift | `a >> k` | floor-divide by 2ᵏ | `12 >> 2 = 3` |

## Tricks worth memorizing

- **Check bit i:** `(n >> i) & 1`
- **Set bit i:** `n | (1 << i)`; **clear bit i:** `n & ~(1 << i)`
- **Is n a power of two?** `n > 0 and n & (n - 1) == 0`
- **Drop the lowest set bit:** `n & (n - 1)`, handy for counting 1-bits
- **XOR cancels pairs:** `x ^ x == 0` and `x ^ 0 == x`, so XOR-ing a list where every number appears twice except one leaves that one.

## Python notes

`bin(13)` gives `'0b1101'`, and `int('1101', 2)` converts back. `n.bit_count()` (Python 3.10+) counts set bits. Python ints have unlimited size, so negative numbers behave as if they had infinitely many leading 1s.

## Bitmasks

An integer can represent a **set** of up to ~60 small items: bit `i` is 1 if item `i` is included. Looping `mask` from `0` to `2ⁿ − 1` enumerates every subset, a common trick in DP.
""",
    "complexity": [
        {"operation": "&, |, ^, ~, <<, >> on fixed-size ints", "time": "O(1)", "space": "O(1)"},
        {"operation": "Count set bits (n & (n − 1) loop)", "time": "O(set bits)", "space": "O(1)"},
        {"operation": "Enumerate all subsets with masks", "time": "O(2ⁿ)", "space": "O(1)"},
        {"operation": "Single Number via XOR", "time": "O(n)", "space": "O(1)"},
    ],
    "snippets": [
        {
            "title": "Reading and changing bits",
            "code": r'''n = 0b1101            # 13

print(bin(n))          # 0b1101
print((n >> 2) & 1)    # bit 2 is 1
print(bin(n | 0b10))   # set bit 1 -> 0b1111
print(bin(n & ~1))     # clear bit 0 -> 0b1100
print(n.bit_count())   # 3 ones


def is_power_of_two(x):
    return x > 0 and x & (x - 1) == 0

print([x for x in range(1, 70) if is_power_of_two(x)])
''',
        },
        {
            "title": "Subsets with bitmasks",
            "code": r'''items = ["a", "b", "c"]

for mask in range(1 << len(items)):
    subset = [items[i] for i in range(len(items)) if mask >> i & 1]
    print(f"{mask:03b}", subset)
''',
        },
    ],
    "problems": [
        {
            "id": "single-number",
            "title": "Single Number",
            "difficulty": "Easy",
            "statement": """
Every number in `nums` appears twice except one. Find it in `O(n)` time and `O(1)` extra space.

**Example**

```
single_number([4, 1, 2, 1, 2])  ->  4
```
""",
            "function": "single_number",
            "starter": "def single_number(nums):\n    pass\n",
            "tests": [
                {"args": [[2, 2, 1]], "expected": 1},
                {"args": [[4, 1, 2, 1, 2]], "expected": 4},
                {"args": [[7]], "expected": 7},
                {"args": [[-3, 5, 5]], "expected": -3},
            ],
            "hints": ["x ^ x == 0 and x ^ 0 == x. What happens if you XOR everything together?"],
            "solution": r'''def single_number(nums):
    result = 0
    for num in nums:
        result ^= num
    return result
''',
        },
        {
            "id": "counting-bits",
            "title": "Counting Bits",
            "difficulty": "Easy",
            "statement": """
Return a list `ans` of length `n + 1` where `ans[i]` is the number of 1-bits in `i`. Try to do it in one pass using earlier answers.

**Example**

```
count_bits(5)  ->  [0, 1, 1, 2, 1, 2]
```
""",
            "function": "count_bits",
            "starter": "def count_bits(n):\n    pass\n",
            "tests": [
                {"args": [2], "expected": [0, 1, 1]},
                {"args": [5], "expected": [0, 1, 1, 2, 1, 2]},
                {"args": [0], "expected": [0]},
                {"args": [8], "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1]},
            ],
            "hints": [
                "i >> 1 is i without its last bit, and you've already computed it.",
                "ans[i] = ans[i >> 1] + (i & 1).",
            ],
            "solution": r'''def count_bits(n):
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans
''',
        },
        {
            "id": "missing-number",
            "title": "Missing Number",
            "difficulty": "Easy",
            "statement": """
`nums` contains `n` distinct numbers from `0..n`, so exactly one is missing. Return it using `O(1)` extra space.

**Example**

```
missing_number([3, 0, 1])  ->  2
```
""",
            "function": "missing_number",
            "starter": "def missing_number(nums):\n    pass\n",
            "tests": [
                {"args": [[3, 0, 1]], "expected": 2},
                {"args": [[0, 1]], "expected": 2},
                {"args": [[9, 6, 4, 2, 3, 5, 7, 0, 1]], "expected": 8},
                {"args": [[1]], "expected": 0},
            ],
            "hints": ["XOR every index 0..n with every value; pairs cancel and the missing one remains."],
            "solution": r'''def missing_number(nums):
    result = len(nums)
    for i, num in enumerate(nums):
        result ^= i ^ num
    return result
''',
        },
    ],
    "quiz": [
        {
            "question": "What is 12 & 10 (1100 & 1010)?",
            "options": ["8", "14", "6", "2"],
            "answer": 0,
            "explanation": "AND keeps only bits set in both: 1000 = 8.",
        },
        {
            "question": "What is 12 ^ 10?",
            "options": ["8", "14", "6", "22"],
            "answer": 2,
            "explanation": "XOR keeps bits that differ: 0110 = 6.",
        },
        {
            "question": "What does n & (n - 1) do?",
            "options": [
                "Doubles n",
                "Clears the lowest set bit of n",
                "Flips every bit",
                "Returns the highest bit",
            ],
            "answer": 1,
            "explanation": "Subtracting 1 flips the lowest 1 and the zeros below it; AND removes that bit.",
        },
        {
            "question": "3 << 3 equals…",
            "options": ["6", "9", "24", "0"],
            "answer": 2,
            "explanation": "Left shift by k multiplies by 2ᵏ: 3 × 8 = 24.",
        },
        {
            "question": "Why does XOR solve Single Number?",
            "options": [
                "XOR sorts the list",
                "Equal numbers cancel (x ^ x = 0), leaving the unique one",
                "XOR finds the maximum",
                "It doesn't; you need a dict",
            ],
            "answer": 1,
            "explanation": "XOR is commutative and associative, so all pairs cancel regardless of order.",
        },
    ],
    "flashcards": [
        {"front": "Check whether bit i of n is set?", "back": "(n >> i) & 1"},
        {"front": "Test if n is a power of two?", "back": "n > 0 and n & (n - 1) == 0"},
        {"front": "What does x ^ x equal? And x ^ 0?", "back": "x ^ x == 0 and x ^ 0 == x, so XOR cancels pairs."},
        {"front": "What do << and >> do arithmetically?", "back": "a << k multiplies by 2ᵏ; a >> k floor-divides by 2ᵏ."},
        {"front": "How do you enumerate all subsets of n items with bits?", "back": "Loop mask from 0 to 2ⁿ − 1; item i is included when (mask >> i) & 1."},
    ],
}
