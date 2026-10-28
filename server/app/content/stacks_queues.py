TOPIC = {
    "id": "stacks-queues",
    "title": "Stacks & Queues",
    "category": "Linear Structures",
    "summary": "LIFO and FIFO structures with list and collections.deque.",
    "visualizer": "stack-queue",
    "lesson": """
Stacks and queues restrict *where* you add and remove items, and that restriction is what makes them useful.

## Stack: last in, first out (LIFO)

Think of a stack of plates. You `push` onto the top and `pop` from the top. A Python `list` is a perfect stack:

```python
stack = []
stack.append(1)   # push
stack.append(2)
stack.pop()       # 2
stack[-1]         # peek → 1
```

**Use a stack when** you need to match or undo the most recent thing: balanced brackets, undo history, depth-first search, evaluating expressions, and *monotonic stack* problems like "next greater element".

## Queue: first in, first out (FIFO)

Think of a line at a shop. You `enqueue` at the back and `dequeue` from the front. Don't use `list.pop(0)` (that's `O(n)`). Use `collections.deque`:

```python
from collections import deque
queue = deque()
queue.append(1)     # enqueue
queue.append(2)
queue.popleft()     # 1
```

**Use a queue when** you process things in arrival order: breadth-first search, task scheduling, sliding windows.

## Monotonic stack

Keep the stack in increasing (or decreasing) order by popping elements that the new item "beats". Each element is pushed and popped at most once, so the whole pass is `O(n)`, a common trick for "next warmer day" or "largest rectangle" problems.
""",
    "complexity": [
        {"operation": "Stack push / pop / peek (list)", "time": "O(1)", "space": "O(1)"},
        {"operation": "Queue append / popleft (deque)", "time": "O(1)", "space": "O(1)"},
        {"operation": "list.pop(0) — avoid!", "time": "O(n)", "space": "O(1)"},
        {"operation": "Search inside stack/queue", "time": "O(n)", "space": "O(1)"},
        {"operation": "Monotonic stack pass", "time": "O(n)", "space": "O(n)"},
    ],
    "snippets": [
        {
            "title": "Balanced brackets with a stack",
            "code": r'''def is_balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


print(is_balanced("{[()]}"))  # True
print(is_balanced("([)]"))    # False
''',
        },
        {
            "title": "Queue with deque",
            "code": r'''from collections import deque

tasks = deque(["write", "test", "ship"])
tasks.append("celebrate")

while tasks:
    print("doing:", tasks.popleft())
''',
        },
    ],
    "problems": [
        {
            "id": "valid-parentheses",
            "title": "Valid Parentheses",
            "difficulty": "Easy",
            "statement": """
Given a string containing only `()[]{}`, return `True` if every opening bracket is closed by the same type, in the correct order.

**Example**

```
is_valid("()[]{}")  ->  True
is_valid("(]")      ->  False
is_valid("([)]")    ->  False
```
""",
            "function": "is_valid",
            "starter": "def is_valid(s):\n    pass\n",
            "tests": [
                {"args": ["()"], "expected": True},
                {"args": ["()[]{}"], "expected": True},
                {"args": ["(]"], "expected": False},
                {"args": ["([)]"], "expected": False},
                {"args": ["{[]}"], "expected": True},
                {"args": ["("], "expected": False},
                {"args": ["]"], "expected": False},
            ],
            "hints": [
                "Push opening brackets onto a stack.",
                "On a closing bracket, the top of the stack must be its matching opener.",
                "At the end the stack must be empty.",
            ],
            "solution": r'''def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
''',
        },
        {
            "id": "min-stack",
            "title": "Min Stack",
            "difficulty": "Medium",
            "statement": """
Design a class `MinStack` supporting these in `O(1)` each:

- `push(val)`
- `pop()`
- `top()` → the top element
- `get_min()` → the smallest element in the stack

Tests call methods in order; the output shows each call's return value (`None` for methods that return nothing).

**Example**

```
s = MinStack()
s.push(-2); s.push(0); s.push(-3)
s.get_min()  ->  -3
s.pop()
s.top()      ->  0
s.get_min()  ->  -2
```
""",
            "function": "MinStack",
            "mode": "design",
            "starter": "class MinStack:\n    def __init__(self):\n        pass\n\n    def push(self, val):\n        pass\n\n    def pop(self):\n        pass\n\n    def top(self):\n        pass\n\n    def get_min(self):\n        pass\n",
            "tests": [
                {"ops": ["MinStack", "push", "push", "push", "get_min", "pop", "top", "get_min"],
                 "args": [[], [-2], [0], [-3], [], [], [], []],
                 "expected": [None, None, None, None, -3, None, 0, -2]},
                {"ops": ["MinStack", "push", "push", "get_min", "pop", "get_min"],
                 "args": [[], [5], [5], [], [], []],
                 "expected": [None, None, None, 5, None, 5]},
            ],
            "hints": [
                "Store pairs `(value, min_so_far)` on the stack.",
                "The current minimum is always in the top pair.",
            ],
            "solution": r'''class MinStack:
    def __init__(self):
        self.stack = []  # (value, min at this depth)

    def push(self, val):
        current_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, current_min))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]
''',
        },
        {
            "id": "daily-temperatures",
            "title": "Daily Temperatures",
            "difficulty": "Medium",
            "statement": """
Given daily temperatures, return a list where `answer[i]` is how many days you wait after day `i` for a **warmer** temperature, or `0` if it never comes.

**Example**

```
daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73])
->  [1, 1, 4, 2, 1, 1, 0, 0]
```
""",
            "function": "daily_temperatures",
            "starter": "def daily_temperatures(temps):\n    pass\n",
            "tests": [
                {"args": [[73, 74, 75, 71, 69, 72, 76, 73]], "expected": [1, 1, 4, 2, 1, 1, 0, 0]},
                {"args": [[30, 40, 50, 60]], "expected": [1, 1, 1, 0]},
                {"args": [[30, 60, 90]], "expected": [1, 1, 0]},
                {"args": [[50, 40, 30]], "expected": [0, 0, 0]},
            ],
            "hints": [
                "Keep a stack of indices of days still waiting for a warmer day.",
                "When today is warmer than the day on top of the stack, pop it and record the gap.",
            ],
            "solution": r'''def daily_temperatures(temps):
    answer = [0] * len(temps)
    waiting = []  # indices with decreasing temperatures
    for i, t in enumerate(temps):
        while waiting and temps[waiting[-1]] < t:
            j = waiting.pop()
            answer[j] = i - j
        waiting.append(i)
    return answer
''',
        },
        {
            'id': 'evaluate-rpn',
            'title': 'Evaluate Reverse Polish Notation',
            'difficulty': 'Medium',
            "statement": """
Evaluate an arithmetic expression in Reverse Polish Notation, given as a list of tokens. Operators are `+ - * /`; division **truncates toward zero**.

**Example**

```
eval_rpn(["2", "1", "+", "3", "*"])  ->  9   ((2 + 1) * 3)
```
""",
            'function': 'eval_rpn',
            'starter': 'def eval_rpn(tokens):\n    pass\n',
            'tests': [{'args': [['2', '1', '+', '3', '*']], 'expected': 9}, {'args': [['4', '13', '5', '/', '+']], 'expected': 6}, {'args': [['10', '6', '9', '3', '+', '-11', '*', '/', '*', '17', '+', '5', '+']], 'expected': 22}],
            'hints': ['Push numbers. On an operator, pop two values, apply it, push the result.', 'The first value popped is the RIGHT operand. Use int(a / b) to truncate toward zero.'],
            'solution': r'''def eval_rpn(tokens):
    stack = []
    for token in tokens:
        if token in ("+", "-", "*", "/"):
            b, a = stack.pop(), stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            else:
                stack.append(int(a / b))
        else:
            stack.append(int(token))
    return stack[0]
''',
        },
        {
            'id': 'largest-rectangle-histogram',
            'title': 'Largest Rectangle in Histogram',
            'difficulty': 'Hard',
            "statement": """
Bars of width 1 have heights `heights`. Return the area of the largest rectangle that fits inside the histogram.

**Example**

```
largest_rectangle_area([2, 1, 5, 6, 2, 3])  ->  10   (bars 5 and 6, height 5 × width 2)
```
""",
            'function': 'largest_rectangle_area',
            'starter': 'def largest_rectangle_area(heights):\n    pass\n',
            'tests': [{'args': [[2, 1, 5, 6, 2, 3]], 'expected': 10}, {'args': [[2, 4]], 'expected': 4}, {'args': [[1]], 'expected': 1}, {'args': [[2, 1, 2]], 'expected': 3}],
            'hints': ['Keep a stack of (start index, height) with increasing heights.', "When a shorter bar arrives, pop taller bars: each popped bar's rectangle ends here.", "A popped bar's start index can be reused by the new shorter bar."],
            'solution': r'''def largest_rectangle_area(heights):
    stack = []  # (start index, height), heights increasing
    best = 0
    for i, h in enumerate(heights + [0]):
        start = i
        while stack and stack[-1][1] > h:
            index, height = stack.pop()
            best = max(best, height * (i - index))
            start = index
        stack.append((start, h))
    return best
''',
        },
    ],
    "quiz": [
        {
            "question": "Which structure is LIFO?",
            "options": ["Queue", "Stack", "Deque", "Heap"],
            "answer": 1,
            "explanation": "Last in, first out: the newest item comes off first.",
        },
        {
            "question": "What's the best way to implement a queue in Python?",
            "options": ["list with pop(0)", "collections.deque", "dict", "set"],
            "answer": 1,
            "explanation": "deque.popleft() is O(1); list.pop(0) is O(n).",
        },
        {
            "question": "Which algorithm naturally uses a queue?",
            "options": ["Depth-first search", "Breadth-first search", "Binary search", "Merge sort"],
            "answer": 1,
            "explanation": "BFS processes nodes level by level, in the order they were discovered.",
        },
        {
            "question": "After push(1), push(2), pop(), push(3) — what is on top of the stack?",
            "options": ["1", "2", "3", "Empty"],
            "answer": 2,
            "explanation": "2 was popped, then 3 was pushed on top of 1.",
        },
        {
            "question": "Why is a monotonic stack pass O(n) even with a while loop inside?",
            "options": [
                "The while loop runs once",
                "Each element is pushed and popped at most once",
                "Python optimizes it",
                "It isn't. It's O(n²)",
            ],
            "answer": 1,
            "explanation": "Total pops across the whole run can't exceed total pushes, which is n.",
        },
    ],
    "flashcards": [
        {'front': 'Stack order?', 'back': 'LIFO: last in, first out. push/pop at the same end.'},
        {'front': 'Queue order?', 'back': 'FIFO: first in, first out. Add at the back, remove from the front.'},
        {'front': 'Best Python queue?', 'back': 'collections.deque with append() and popleft(), both O(1).'},
        {'front': 'Classic stack problems?', 'back': 'Matching brackets, undo, DFS, expression evaluation, monotonic stack (next greater element).'},
        {'front': 'Why is a monotonic stack pass O(n)?', 'back': 'Each element is pushed once and popped at most once.'},
    ],
}
