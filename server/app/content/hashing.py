TOPIC = {
    "id": "hashing",
    "title": "Hash Maps & Sets",
    "category": "Linear Structures",
    "summary": "Python dict and set: O(1) lookups that power countless solutions.",
    "visualizer": "hash-table",
    "lesson": """
A **hash table** maps keys to values using a *hash function* that turns each key into a bucket index. Because the index is computed rather than searched for, lookups, inserts and deletes take **`O(1)` on average**.

Python gives you two hash-based types:

- `dict`: key → value pairs, e.g. `{"apple": 3}`
- `set`: unique keys only, e.g. `{1, 2, 3}`

## How it works

1. Compute `hash(key)`, a large integer.
2. Map it to a bucket: `index = hash(key) % number_of_buckets`.
3. Store the entry there. If two keys land in the same bucket (*a collision*), the table keeps both, either by chaining them in a small list or by probing for the next free slot.

When the table gets too full, it **resizes** (usually doubling) and re-inserts everything. This occasional `O(n)` step averages out, so operations stay `O(1)` amortized.

## Keys must be hashable

Only immutable values can be keys: `int`, `str`, `tuple` work; `list` and `dict` don't. Use `tuple(sorted(word))` as a key to group anagrams.

## Patterns to recognize

- **"Have I seen this before?"**: use a `set`.
- **Counting**: `collections.Counter(nums)` or `counts[x] = counts.get(x, 0) + 1`.
- **Complement lookup**: for two-sum, store each number's index and check whether `target - num` already exists.
- **Grouping**: `collections.defaultdict(list)` keyed by a canonical form.
""",
    "complexity": [
        {"operation": "d[key], key in d, d[key] = v", "time": "O(1) avg", "space": "O(1)"},
        {"operation": "del d[key], set.add, set.remove", "time": "O(1) avg", "space": "O(1)"},
        {"operation": "Worst case (all keys collide)", "time": "O(n)", "space": "—"},
        {"operation": "Iterate over all entries", "time": "O(n)", "space": "O(1)"},
        {"operation": "Build from n items", "time": "O(n)", "space": "O(n)"},
    ],
    "snippets": [
        {
            "title": "A tiny hash table with chaining",
            "code": r'''class HashTable:
    def __init__(self, size=8):
        self.buckets = [[] for _ in range(size)]

    def _index(self, key):
        return hash(key) % len(self.buckets)

    def put(self, key, value):
        bucket = self.buckets[self._index(key)]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value     # update existing key
                return
        bucket.append([key, value])  # collision → chain

    def get(self, key):
        for k, v in self.buckets[self._index(key)]:
            if k == key:
                return v
        raise KeyError(key)


table = HashTable()
table.put("apple", 3)
table.put("pear", 5)
print(table.get("pear"))  # 5
''',
        },
        {
            "title": "Counting with Counter and dict",
            "code": r'''from collections import Counter

words = ["cat", "dog", "cat", "bird", "cat"]

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)                    # {'cat': 3, 'dog': 1, 'bird': 1}

print(Counter(words).most_common(1))  # [('cat', 3)]
''',
        },
    ],
    "problems": [
        {
            "id": "two-sum",
            "title": "Two Sum",
            "difficulty": "Easy",
            "statement": """
Given a list `nums` (not sorted) and a `target`, return the indices `[i, j]` with `i < j` of the two numbers that add up to `target`. Exactly one answer exists.

Aim for `O(n)` time.

**Example**

```
two_sum([2, 7, 11, 15], 9)  ->  [0, 1]
two_sum([3, 2, 4], 6)       ->  [1, 2]
```
""",
            "function": "two_sum",
            "starter": "def two_sum(nums, target):\n    pass\n",
            "tests": [
                {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
                {"args": [[3, 2, 4], 6], "expected": [1, 2]},
                {"args": [[3, 3], 6], "expected": [0, 1]},
                {"args": [[-1, -2, -3, -4, -5], -8], "expected": [2, 4]},
            ],
            "hints": [
                "For each number, the partner you need is `target - num`.",
                "Store each number's index in a dict as you go, and check the dict before inserting.",
            ],
            "solution": r'''def two_sum(nums, target):
    index_of = {}
    for i, num in enumerate(nums):
        if target - num in index_of:
            return [index_of[target - num], i]
        index_of[num] = i
    return []
''',
        },
        {
            "id": "group-anagrams",
            "title": "Group Anagrams",
            "difficulty": "Medium",
            "statement": """
Group the words in `words` that are anagrams of each other. Return a list of groups; the order of groups and of words inside each group doesn't matter.

**Example**

```
group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
->  [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
```
""",
            "function": "group_anagrams",
            "compare": "unordered_nested",
            "starter": "def group_anagrams(words):\n    pass\n",
            "tests": [
                {"args": [["eat", "tea", "tan", "ate", "nat", "bat"]],
                 "expected": [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]},
                {"args": [[""]], "expected": [[""]]},
                {"args": [["a"]], "expected": [["a"]]},
                {"args": [["abc", "bca", "xyz"]], "expected": [["abc", "bca"], ["xyz"]]},
            ],
            "hints": [
                "Anagrams become identical when their letters are sorted.",
                "Use `tuple(sorted(word))` as a dict key and append each word to its group.",
            ],
            "solution": r'''from collections import defaultdict


def group_anagrams(words):
    groups = defaultdict(list)
    for word in words:
        groups[tuple(sorted(word))].append(word)
    return list(groups.values())
''',
        },
        {
            "id": "first-unique-char",
            "title": "First Unique Character",
            "difficulty": "Easy",
            "statement": """
Return the index of the first character in `s` that appears exactly once, or `-1` if there is none.

**Example**

```
first_unique_char("leetcode")      ->  0
first_unique_char("loveleetcode")  ->  2
first_unique_char("aabb")          ->  -1
```
""",
            "function": "first_unique_char",
            "starter": "def first_unique_char(s):\n    pass\n",
            "tests": [
                {"args": ["leetcode"], "expected": 0},
                {"args": ["loveleetcode"], "expected": 2},
                {"args": ["aabb"], "expected": -1},
                {"args": ["z"], "expected": 0},
            ],
            "hints": ["Count every character first, then scan the string again for a count of 1."],
            "solution": r'''from collections import Counter


def first_unique_char(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
''',
        },
    ],
    "quiz": [
        {
            "question": "What is the average time to check `x in my_set`?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
            "answer": 0,
            "explanation": "The hash of x points straight to its bucket.",
        },
        {
            "question": "Which of these can be used as a dict key?",
            "options": ["[1, 2]", "{'a': 1}", "(1, 2)", "{1, 2}"],
            "answer": 2,
            "explanation": "Keys must be hashable (immutable). Tuples are; lists, dicts and sets are not.",
        },
        {
            "question": "What is a collision?",
            "options": [
                "Two keys with the same value",
                "Two different keys mapping to the same bucket",
                "Inserting a duplicate key",
                "Running out of memory",
            ],
            "answer": 1,
            "explanation": "The table resolves collisions by chaining or probing.",
        },
        {
            "question": "Why do hash tables resize?",
            "options": [
                "To sort the keys",
                "To keep buckets short so lookups stay O(1)",
                "To free memory",
                "Python requires it every 100 inserts",
            ],
            "answer": 1,
            "explanation": "As the load factor grows, chains get longer; resizing spreads entries out again.",
        },
        {
            "question": "In Two Sum, what do you store in the dictionary?",
            "options": [
                "Each index → its number",
                "Each number → its index",
                "Each pair's sum",
                "Only the target",
            ],
            "answer": 1,
            "explanation": "Then `target - num` can be looked up in O(1) to find the partner's index.",
        },
    ],
}
