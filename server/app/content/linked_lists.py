TOPIC = {
    "id": "linked-lists",
    "title": "Linked Lists",
    "category": "Linear Structures",
    "summary": "Nodes connected by pointers: reversing, merging, and fast/slow tricks.",
    "visualizer": "linked-list",
    "lesson": """
A **linked list** is a chain of nodes. Each node holds a value and a reference (`next`) to the following node. The list is identified by its **head**; the last node points to `None`.

```
head → [3] → [7] → [1] → None
```

## Arrays vs linked lists

| | Array (`list`) | Linked list |
| --- | --- | --- |
| Access i-th item | `O(1)` | `O(n)`, must walk from head |
| Insert/delete at front | `O(n)` | `O(1)` |
| Insert/delete after a known node | `O(n)` | `O(1)` |
| Memory | Contiguous | Scattered + pointer overhead |

## The node class

In problems on this site, `ListNode` is already defined:

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
```

## Essential techniques

- **Dummy head**: create `dummy = ListNode()` and build after it, then return `dummy.next`. This removes special cases for an empty result.
- **Reversal**: walk the list with `prev`, `curr`; at each step point `curr.next` back to `prev`. Always save `curr.next` *before* overwriting it.
- **Fast & slow pointers**: move `slow` one step and `fast` two steps. When `fast` reaches the end, `slow` is at the middle. If they ever meet, the list has a cycle (Floyd's algorithm).

## Common mistakes

Losing the rest of the list by overwriting `next` too early, and forgetting to handle `None` (empty list or reaching the end). Draw the boxes and arrows on paper; it really helps.
""",
    "complexity": [
        {"operation": "Access / search", "time": "O(n)", "space": "O(1)"},
        {"operation": "Insert / delete at head", "time": "O(1)", "space": "O(1)"},
        {"operation": "Insert after a given node", "time": "O(1)", "space": "O(1)"},
        {"operation": "Reverse (iterative)", "time": "O(n)", "space": "O(1)"},
        {"operation": "Find middle (fast/slow)", "time": "O(n)", "space": "O(1)"},
    ],
    "snippets": [
        {
            "title": "Build, print and reverse a list",
            "code": r'''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build(values):
    dummy = ListNode()
    tail = dummy
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next


def to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


def reverse(head):
    prev = None
    curr = head
    while curr:
        nxt = curr.next      # save the rest
        curr.next = prev     # flip the arrow
        prev = curr
        curr = nxt
    return prev


print(to_list(reverse(build([1, 2, 3, 4]))))  # [4, 3, 2, 1]
''',
        },
        {
            "title": "Detect a cycle (Floyd's tortoise and hare)",
            "code": r'''def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
''',
        },
    ],
    "problems": [
        {
            "id": "reverse-linked-list",
            "title": "Reverse Linked List",
            "difficulty": "Easy",
            "statement": """
Reverse a singly linked list and return the new head. `ListNode` is predefined.

Tests pass and compare lists as Python lists for readability; your function receives and returns real `ListNode`s.

**Example**

```
1 → 2 → 3 → 4 → 5   becomes   5 → 4 → 3 → 2 → 1
```
""",
            "function": "reverse_list",
            "arg_types": ["linked_list"],
            "return_type": "linked_list",
            "starter": "def reverse_list(head):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4, 5]], "expected": [5, 4, 3, 2, 1]},
                {"args": [[1, 2]], "expected": [2, 1]},
                {"args": [[]], "expected": []},
            ],
            "hints": [
                "Keep `prev = None` and `curr = head`.",
                "Save `curr.next`, point `curr.next` at `prev`, then advance both pointers.",
            ],
            "solution": r'''def reverse_list(head):
    prev, curr = None, head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt
    return prev
''',
        },
        {
            "id": "merge-two-sorted-lists",
            "title": "Merge Two Sorted Lists",
            "difficulty": "Easy",
            "statement": """
Merge two sorted linked lists into one sorted list by splicing their nodes together. Return the head of the merged list.

**Example**

```
merge_two_lists(1 → 2 → 4, 1 → 3 → 4)  ->  1 → 1 → 2 → 3 → 4 → 4
```
""",
            "function": "merge_two_lists",
            "arg_types": ["linked_list", "linked_list"],
            "return_type": "linked_list",
            "starter": "def merge_two_lists(a, b):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 4], [1, 3, 4]], "expected": [1, 1, 2, 3, 4, 4]},
                {"args": [[], []], "expected": []},
                {"args": [[], [0]], "expected": [0]},
                {"args": [[5], [1, 2, 3]], "expected": [1, 2, 3, 5]},
            ],
            "hints": [
                "Use a dummy head and a `tail` pointer.",
                "Attach the smaller head each time; when one list runs out, attach the rest of the other.",
            ],
            "solution": r'''def merge_two_lists(a, b):
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b
    return dummy.next
''',
        },
        {
            "id": "middle-of-linked-list",
            "title": "Middle of the Linked List",
            "difficulty": "Easy",
            "statement": """
Return the middle node of the list. If there are two middle nodes, return the **second** one. (The test shows the list starting from the node you return.)

**Example**

```
1 → 2 → 3 → 4 → 5       ->  3 → 4 → 5
1 → 2 → 3 → 4 → 5 → 6   ->  4 → 5 → 6
```
""",
            "function": "middle_node",
            "arg_types": ["linked_list"],
            "return_type": "linked_list",
            "starter": "def middle_node(head):\n    pass\n",
            "tests": [
                {"args": [[1, 2, 3, 4, 5]], "expected": [3, 4, 5]},
                {"args": [[1, 2, 3, 4, 5, 6]], "expected": [4, 5, 6]},
                {"args": [[1]], "expected": [1]},
            ],
            "hints": ["Move `slow` one step and `fast` two steps until `fast` can't move."],
            "solution": r'''def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
''',
        },
        {
            'id': 'remove-nth-from-end',
            'title': 'Remove Nth Node From End',
            'difficulty': 'Medium',
            "statement": """
Remove the `n`-th node from the end of the list and return its head, in one pass.

**Example**

```
remove_nth_from_end(1 → 2 → 3 → 4 → 5, 2)  ->  1 → 2 → 3 → 5
```
""",
            'function': 'remove_nth_from_end',
            'arg_types': ['linked_list', None],
            'return_type': 'linked_list',
            'starter': 'def remove_nth_from_end(head, n):\n    pass\n',
            'tests': [{'args': [[1, 2, 3, 4, 5], 2], 'expected': [1, 2, 3, 5]}, {'args': [[1], 1], 'expected': []}, {'args': [[1, 2], 1], 'expected': [1]}, {'args': [[1, 2], 2], 'expected': [2]}],
            'hints': ["Use a dummy node so removing the head isn't a special case.", 'Move `fast` n + 1 steps ahead, then move both until `fast` is None.'],
            'solution': r'''def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
''',
        },
        {
            'id': 'add-two-numbers',
            'title': 'Add Two Numbers',
            'difficulty': 'Medium',
            "statement": """
Two non-negative integers are stored as linked lists of digits in **reverse** order (`342` is `2 → 4 → 3`). Return their sum as a list in the same format.

**Example**

```
add_two_numbers(2 → 4 → 3, 5 → 6 → 4)  ->  7 → 0 → 8   (342 + 465 = 807)
```
""",
            'function': 'add_two_numbers',
            'arg_types': ['linked_list', 'linked_list'],
            'return_type': 'linked_list',
            'starter': 'def add_two_numbers(a, b):\n    pass\n',
            'tests': [{'args': [[2, 4, 3], [5, 6, 4]], 'expected': [7, 0, 8]}, {'args': [[0], [0]], 'expected': [0]}, {'args': [[9, 9, 9, 9], [9, 9]], 'expected': [8, 9, 0, 0, 1]}],
            'hints': ['Walk both lists together, like adding by hand from the ones digit.', 'Keep going while either list or the carry remains.'],
            'solution': r'''def add_two_numbers(a, b):
    dummy = tail = ListNode()
    carry = 0
    while a or b or carry:
        total = carry + (a.val if a else 0) + (b.val if b else 0)
        carry, digit = divmod(total, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        a = a.next if a else None
        b = b.next if b else None
    return dummy.next
''',
        },
    ],
    "quiz": [
        {
            "question": "What is the time to access the 50th node of a linked list?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
            "answer": 2,
            "explanation": "There's no index; you must follow next pointers from the head.",
        },
        {
            "question": "When reversing a list, why save curr.next before changing it?",
            "options": [
                "It makes the code faster",
                "Otherwise you lose the reference to the rest of the list",
                "Python requires it",
                "To detect cycles",
            ],
            "answer": 1,
            "explanation": "After curr.next = prev, the only link to the remaining nodes is gone.",
        },
        {
            "question": "What is a dummy head used for?",
            "options": [
                "Storing the list length",
                "Avoiding special cases when the result may be empty or the head changes",
                "Making the list circular",
                "Speeding up search",
            ],
            "answer": 1,
            "explanation": "You always have a node to attach to, then return dummy.next.",
        },
        {
            "question": "With slow moving 1 step and fast moving 2, where is slow when fast reaches the end?",
            "options": ["At the head", "At the middle", "At the end", "One before the end"],
            "answer": 1,
            "explanation": "fast covers twice the distance, so slow has gone halfway.",
        },
        {
            "question": "Which operation is faster on a linked list than on a Python list?",
            "options": ["Access by index", "Insert at the front", "Binary search", "Sorting"],
            "answer": 1,
            "explanation": "Inserting a new head is O(1); list.insert(0, x) is O(n).",
        },
    ],
    "flashcards": [
        {'front': 'Time to access the k-th node of a linked list?', 'back': 'O(k): you must follow next pointers from the head.'},
        {'front': 'Why use a dummy head node?', 'back': 'So inserting/removing at the head needs no special case; return dummy.next.'},
        {'front': 'The 3 pointer moves to reverse a list?', 'back': 'nxt = curr.next; curr.next = prev; prev, curr = curr, nxt.'},
        {'front': 'How do you find the middle in one pass?', 'back': 'slow moves 1 step, fast moves 2; when fast ends, slow is at the middle.'},
        {'front': 'How do you detect a cycle?', 'back': "Floyd's tortoise and hare: if slow and fast pointers ever meet, there's a cycle."},
    ],
}
