TOPIC = {
    "id": "tries",
    "title": "Tries (Prefix Trees)",
    "category": "Trees & Graphs",
    "summary": "Store words letter by letter for lightning-fast prefix lookups.",
    "visualizer": "trie",
    "lesson": """
A **trie** (pronounced "try") is a tree where each edge is a character and each path from the root spells a prefix. Words that share a prefix share the same path, so "car", "cart" and "care" all start down `c → a → r`.

```python
class TrieNode:
    def __init__(self):
        self.children = {}     # char -> TrieNode
        self.is_word = False   # does a word end here?
```

## Operations

- **Insert**: walk the word letter by letter, creating missing children, then mark the last node `is_word = True`.
- **Search**: walk the word; it's present only if every letter exists **and** the final node has `is_word`.
- **Starts with**: like search, but you don't need `is_word`; the path existing is enough.

All three take `O(L)` time, where `L` is the word's length, **no matter how many words** are stored. A hash set can also check whole words in `O(L)`, but can't answer "which words start with `ca`?" without scanning everything.

## Where tries shine

- Autocomplete and spell-check suggestions
- Prefix counting ("how many words start with `pre`?")
- Word games and searching many words in a grid at once
- IP routing (longest prefix match)

## Trade-offs

Tries use more memory than a set because every node holds a dict of children. A compact alternative is a nested dict: `trie = {}` and `node = node.setdefault(ch, {})`, with a special key like `"$"` marking word ends.
""",
    "complexity": [
        {"operation": "Insert word of length L", "time": "O(L)", "space": "O(L) new nodes"},
        {"operation": "Search / starts_with", "time": "O(L)", "space": "O(1)"},
        {"operation": "Store N words of average length L", "time": "O(N·L)", "space": "O(N·L)"},
        {"operation": "List all words with a prefix", "time": "O(L + matches)", "space": "O(matches)"},
    ],
    "snippets": [
        {
            "title": "Trie with insert, search and starts_with",
            "code": r'''class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True                  # end-of-word marker

    def _walk(self, text):
        node = self.root
        for ch in text:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix):
        return self._walk(prefix) is not None


t = Trie()
for w in ["car", "cart", "care", "dog"]:
    t.insert(w)
print(t.search("car"), t.search("ca"), t.starts_with("ca"))  # True False True
''',
        },
        {
            "title": "Autocomplete: all words with a prefix",
            "code": r'''def words_with_prefix(root, prefix):
    node = root
    for ch in prefix:
        if ch not in node:
            return []
        node = node[ch]

    results = []

    def collect(n, path):
        if "$" in n:
            results.append(prefix + path)
        for ch, child in n.items():
            if ch != "$":
                collect(child, path + ch)

    collect(node, "")
    return sorted(results)


root = {}
for w in ["tree", "trie", "trip", "tea"]:
    node = root
    for ch in w:
        node = node.setdefault(ch, {})
    node["$"] = True
print(words_with_prefix(root, "tri"))  # ['trie', 'trip']
''',
        },
    ],
    "problems": [
        {
            "id": "implement-trie",
            "title": "Implement Trie",
            "difficulty": "Medium",
            "statement": """
Design a `Trie` class with:

- `insert(word)`
- `search(word)` → `True` if the exact word was inserted
- `starts_with(prefix)` → `True` if any inserted word starts with `prefix`

**Example**

```
t = Trie()
t.insert("apple")
t.search("apple")    ->  True
t.search("app")      ->  False
t.starts_with("app") ->  True
t.insert("app")
t.search("app")      ->  True
```
""",
            "function": "Trie",
            "mode": "design",
            "starter": "class Trie:\n    def __init__(self):\n        pass\n\n    def insert(self, word):\n        pass\n\n    def search(self, word):\n        pass\n\n    def starts_with(self, prefix):\n        pass\n",
            "tests": [
                {"ops": ["Trie", "insert", "search", "search", "starts_with", "insert", "search"],
                 "args": [[], ["apple"], ["apple"], ["app"], ["app"], ["app"], ["app"]],
                 "expected": [None, None, True, False, True, None, True]},
                {"ops": ["Trie", "insert", "starts_with", "search", "starts_with"],
                 "args": [[], ["dog"], ["do"], ["cat"], ["cat"]],
                 "expected": [None, None, True, False, False]},
            ],
            "hints": [
                "Each node needs a dict of children and a flag saying whether a word ends there.",
                "search and starts_with share the same walk; only the final check differs.",
            ],
            "solution": r'''class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def _walk(self, text):
        node = self.root
        for ch in text:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix):
        return self._walk(prefix) is not None
''',
        },
        {
            "id": "longest-common-prefix",
            "title": "Longest Common Prefix",
            "difficulty": "Easy",
            "statement": """
Return the longest prefix shared by every string in `words`, or `""` if there is none.

**Example**

```
longest_common_prefix(["flower", "flow", "flight"])  ->  "fl"
```
""",
            "function": "longest_common_prefix",
            "starter": "def longest_common_prefix(words):\n    pass\n",
            "tests": [
                {"args": [["flower", "flow", "flight"]], "expected": "fl"},
                {"args": [["dog", "racecar", "car"]], "expected": ""},
                {"args": [["alone"]], "expected": "alone"},
                {"args": [["ab", "a"]], "expected": "a"},
            ],
            "hints": [
                "Compare character by character across all words.",
                "Or: insert into a trie and walk down while each node has exactly one child and no word ends.",
            ],
            "solution": r'''def longest_common_prefix(words):
    prefix = words[0]
    for word in words[1:]:
        while not word.startswith(prefix):
            prefix = prefix[:-1]
    return prefix
''',
        },
        {
            "id": "replace-words",
            "title": "Replace Words",
            "difficulty": "Medium",
            "statement": """
Given a list of `roots` and a `sentence`, replace every word with the **shortest** root that is its prefix (leave it unchanged if none). Return the new sentence.

**Example**

```
replace_words(["cat", "bat", "rat"], "the cattle was rattled by the battery")
->  "the cat was rat by the bat"
```
""",
            "function": "replace_words",
            "starter": "def replace_words(roots, sentence):\n    pass\n",
            "tests": [
                {"args": [["cat", "bat", "rat"], "the cattle was rattled by the battery"],
                 "expected": "the cat was rat by the bat"},
                {"args": [["a", "b", "c"], "aadsfasf absbs bbab cadsfafs"], "expected": "a a b c"},
                {"args": [["ab", "a"], "abc"], "expected": "a"},
            ],
            "hints": [
                "Insert all roots into a trie.",
                "For each word, walk the trie and stop at the first node that ends a root.",
            ],
            "solution": r'''def replace_words(roots, sentence):
    trie = {}
    for root in roots:
        node = trie
        for ch in root:
            node = node.setdefault(ch, {})
        node["$"] = True

    def shortest_root(word):
        node = trie
        for i, ch in enumerate(word):
            if ch not in node:
                return word
            node = node[ch]
            if "$" in node:
                return word[:i + 1]
        return word

    return " ".join(shortest_root(word) for word in sentence.split())
''',
        },
    ],
    "quiz": [
        {
            "question": "What does each edge in a trie represent?",
            "options": ["A whole word", "A single character", "A word's length", "A hash value"],
            "answer": 1,
            "explanation": "Paths from the root spell prefixes, one character per edge.",
        },
        {
            "question": "Time to search a word of length L in a trie with N words?",
            "options": ["O(N)", "O(L)", "O(N·L)", "O(log N)"],
            "answer": 1,
            "explanation": "You follow one edge per character, independent of N.",
        },
        {
            "question": "After inserting only 'apple', what does search('app') return?",
            "options": ["True", "False", "An error", "'apple'"],
            "answer": 1,
            "explanation": "The path exists, but no word ends at the second 'p', so is_word is False.",
        },
        {
            "question": "What can a trie do that a hash set can't do efficiently?",
            "options": [
                "Check if a word exists",
                "Find all words with a given prefix",
                "Store strings",
                "Delete words",
            ],
            "answer": 1,
            "explanation": "A set would have to scan every word to answer prefix queries.",
        },
        {
            "question": "Main downside of tries?",
            "options": ["Slow lookups", "Higher memory use", "Can't store duplicates", "Only work on numbers"],
            "answer": 1,
            "explanation": "Every node carries its own children map.",
        },
    ],
    "flashcards": [
        {"front": "What's stored in a trie node?", "back": "A map of child characters → nodes, and an is_word flag."},
        {"front": "search vs starts_with in a trie?", "back": "Both walk the path; search also requires the last node to be marked as a word end."},
        {"front": "Time to insert/search a word of length L?", "back": "O(L), regardless of how many words are stored."},
        {"front": "Name three uses of tries.", "back": "Autocomplete, spell-check/prefix counting, word search in grids (also IP longest-prefix routing)."},
        {"front": "Quick trie in Python without a class?", "back": "Nested dicts: node = node.setdefault(ch, {}), with a '$' key marking word ends."},
    ],
}
