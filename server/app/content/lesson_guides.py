"""Beginner-friendly additions to each lesson: id -> (intro, walkthrough, mistakes, when to use)."""

GUIDES = {
    "big-o": (
        """Imagine finding a friend's name in a phone book. Reading every page from the start takes longer as the book gets thicker. Opening the middle and repeatedly discarding half barely slows down, even for a huge book. **Big-O is a way of describing that difference**: not how many seconds code takes, but how the work grows when the input grows.""",
        """How many steps does each approach take to check a list of `n` numbers for duplicates?

| n | Compare every pair (`O(n²)`) | Use a set (`O(n)`) |
| --- | --- | --- |
| 10 | about 45 | 10 |
| 1,000 | about 500,000 | 1,000 |
| 100,000 | about 5,000,000,000 | 100,000 |

With 10 items both feel instant. With 100,000 items, one finishes immediately and the other can run for minutes. To find the complexity of your own code, ask: **how many times does the innermost line run as `n` grows?**""",
        [
            "Counting only your own loops. `x in my_list`, `nums.pop(0)` and `nums[a:b]` all hide a loop inside them.",
            "Forgetting memory. Creating a new list of size n costs O(n) space.",
            "Assuming a faster class always wins on tiny inputs. Big-O describes growth, so it matters most as n gets large.",
        ],
        "Use it every time you finish a solution: state its time and space, then ask whether the input size allows it. A rough guide is that about 100 million simple steps fit in a second or so in fast languages, and Python manages noticeably fewer.",
    ),
    "bit-manipulation": (
        """Think of a number as a row of light switches, where each switch is worth double the one to its right (1, 2, 4, 8…). `13` means the switches for 8, 4 and 1 are on: `1101`. **Bit manipulation means flipping and comparing those switches directly**, which is very fast and sometimes makes a hard-looking problem take just one line.""",
        """Find the number that appears once in `[4, 1, 2, 1, 2]` using XOR (`^`), which gives 0 for two equal numbers:

| Step | Number | result after `result ^= number` |
| --- | --- | --- |
| start | | 0 |
| 1 | 4 | 4 |
| 2 | 1 | 5 |
| 3 | 2 | 7 |
| 4 | 1 | 6 |
| 5 | 2 | 4 |

The two 1s cancelled and the two 2s cancelled, leaving **4**. Order doesn't matter.""",
        [
            "Mixing up operator precedence. `x & 1 == 0` compares first, so write `(x & 1) == 0`.",
            "Confusing `^` with power. In Python `2 ^ 3` is XOR (1); power is `2 ** 3`.",
            "Expecting `~x` to be a positive flip. In Python `~12` is -13.",
        ],
        "Reach for bits when a problem mentions pairs that cancel, powers of two, or \"use O(1) space\", or when you need to represent a small set of items as one number.",
    ),
    "arrays": (
        """An array is like a row of numbered lockers. Because the lockers are side by side, you can go straight to locker 500 without opening the others. But adding a locker in the middle means moving everything after it. **The two-pointer trick is like two people walking along the row**, so you don't have to compare every pair of lockers.""",
        """Find two numbers adding to 10 in the sorted list `[1, 3, 4, 6, 8, 11]`:

| left | right | Sum | Decision |
| --- | --- | --- | --- |
| 1 | 11 | 12 | Too big, move right inward |
| 1 | 8 | 9 | Too small, move left inward |
| 3 | 8 | 11 | Too big, move right inward |
| 3 | 6 | 9 | Too small, move left inward |
| 4 | 6 | 10 | Found it! |

Five checks instead of up to 15 pairs. It works because the list is sorted, so each move safely rules out numbers.""",
        [
            "Using opposite-end pointers on unsorted data. Sort first, or use a hash map.",
            "Off-by-one errors: the last index is `len(nums) - 1`, not `len(nums)`.",
            "Changing a list's size while looping over it, which skips items.",
        ],
        "Try two pointers when the data is sorted, when you compare both ends (palindromes), or when you must rearrange a list in place.",
    ),
    "sliding-window": (
        """Picture a magnifying glass sliding along a line of text: you only see a section at a time. When it moves one letter right, one letter enters and one may leave, so **you update what you know instead of re-reading everything**. That is the whole idea of a sliding window.""",
        """Longest stretch with no repeated letters in `"abcab"`:

| right | New letter | Action | Window | Best |
| --- | --- | --- | --- | --- |
| 0 | a | Add | `a` | 1 |
| 1 | b | Add | `ab` | 2 |
| 2 | c | Add | `abc` | 3 |
| 3 | a | Repeat: drop `a` from the left | `bca` | 3 |
| 4 | b | Repeat: drop `b` from the left | `cab` | 3 |

The answer is **3**. Each letter joined and left the window at most once, so the work is O(n).""",
        [
            "Rebuilding the window's total or counts from scratch each step, which loses the speed advantage.",
            "Using `if` to shrink when you may need to remove several items. Use `while`.",
            "Applying it to sums with negative numbers, where shrinking doesn't reliably lower the sum.",
        ],
        "Look for the words **contiguous**, **substring** or **subarray**, combined with longest, shortest, or \"of size k\".",
    ),
    "hashing": (
        """Think of a library where a formula tells you the exact shelf for any book title. You don't search shelf by shelf; you compute the location and walk straight there. **A hash map does this for data**: the key is turned into a shelf number, which is why Python's `dict` and `set` feel instant.""",
        """Two Sum on `[2, 7, 11]` with target 9. For each number, ask: \"have I already seen the partner I need?\"

| i | num | Need | In `seen`? | `seen` afterwards |
| --- | --- | --- | --- | --- |
| 0 | 2 | 7 | No | `{2: 0}` |
| 1 | 7 | 2 | **Yes, at index 0** | Return `[0, 1]` |

One pass, instead of comparing every pair. We traded a little memory for a lot of speed.""",
        [
            "Using a list as a key. Lists can change, so convert with `tuple(my_list)`.",
            "Reading `counts[x]` for a missing key, which raises `KeyError`. Use `counts.get(x, 0)` or `Counter`.",
            "Using a dict or set when you need sorted order; they don't keep items sorted.",
        ],
        "Use one whenever you catch yourself asking \"have I seen this?\", \"how many of these?\" or \"which items belong together?\".",
    ),
    "linked-lists": (
        """A linked list is a treasure hunt: each clue holds a value and tells you where the next clue is. You can't jump to clue 50; you must follow them in order. But adding a new clue is easy, because **you only rewrite one or two \"next\" directions** and nothing else has to move.""",
        """Reversing `1 → 2 → 3`:

| Step | prev | curr | What happens |
| --- | --- | --- | --- |
| Start | None | 1 | |
| 1 | 1 | 2 | 1 now points to None |
| 2 | 2 | 3 | 2 now points to 1 |
| 3 | 3 | None | 3 now points to 2 |

`curr` is empty, so return `prev`: `3 → 2 → 1`. The Visualize tab animates exactly this.""",
        [
            "Overwriting `curr.next` before saving it, which loses the rest of the list.",
            "Reading `node.next.val` without checking `node.next` isn't None.",
            "Returning the old `head` after reversing; it's now the last node.",
        ],
        "Use linked lists for frequent inserts and removals at known positions, or when a problem gives you `ListNode`s. In everyday Python, a `list` or `deque` is usually simpler.",
    ),
    "stacks-queues": (
        """A **stack** is a pile of plates: the last plate you put on is the first you take off. A **queue** is a line at a shop: the first person to arrive is served first. Same items, but the rule about who leaves next changes what problems they solve.""",
        """Checking brackets in `"([])"` with a stack:

| Character | Action | Stack |
| --- | --- | --- |
| `(` | Push | `(` |
| `[` | Push | `( [` |
| `]` | Top is `[`, a match: pop | `(` |
| `)` | Top is `(`, a match: pop | empty |

The stack ends empty, so the brackets are valid. A stack fits because **the most recently opened bracket must close first**.""",
        [
            "Calling `pop()` on an empty stack. Check `if stack:` first.",
            "Using `list.pop(0)` for a queue, which is O(n). Use `deque.popleft()`.",
            "Forgetting to check the stack is empty at the end, which wrongly accepts `\"((\"`.",
        ],
        "Use a stack for \"most recent first\": matching, undo, or next greater element. Use a queue for \"in arrival order\": BFS and task processing.",
    ),
    "recursion": (
        """Imagine standing in a long queue and wanting to know your position. You ask the person ahead, who asks the person ahead of them, until the first person says \"I'm number 1\". The answers then come back: 2, 3, 4… **Recursion is the same: a function hands a smaller version of the job to itself**, until the job is small enough to answer directly.""",
        """How `factorial(3)` runs:

```
factorial(3)  waits for factorial(2)
  factorial(2)  waits for factorial(1)
    factorial(1)  base case, returns 1
  factorial(2)  returns 2 × 1 = 2
factorial(3)  returns 3 × 2 = 6
```

Calls go **down** until the base case, and answers come back **up**. Backtracking uses the same shape, adding \"undo my choice\" on the way back.""",
        [
            "A missing or unreachable base case, which ends in `RecursionError`.",
            "Forgetting `return` before the recursive call, so the answer is lost and you get None.",
            "Appending `path` instead of `path[:]` in backtracking, so every saved answer changes later.",
        ],
        "Use it when a problem contains smaller copies of itself (trees, nested data), or when you must explore all combinations.",
    ),
    "sorting": (
        """Think about sorting playing cards. You might repeatedly swap neighbours (bubble sort), pick out the smallest each time (selection sort), or slide each new card into your sorted hand (insertion sort). Or, with a big deck, split it between friends and merge their sorted piles (merge sort). **All reach the same result, but they differ hugely in effort on big inputs.**""",
        """Merge sort on `[5, 2, 4, 1]`:

```
Split:   [5, 2]        [4, 1]
Split:   [5] [2]       [4] [1]
Merge:   [2, 5]        [1, 4]
Merge:   compare heads 2 and 1, take 1
         compare 2 and 4, take 2
         compare 5 and 4, take 4
         take the remaining 5
Result:  [1, 2, 4, 5]
```

There are about log n levels of splitting, and each level does about n work, which gives **O(n log n)**.""",
        [
            "Writing `nums = nums.sort()`. `sort()` returns None, so use `nums.sort()` or `sorted(nums)`.",
            "Forgetting to add the leftovers after a merge loop.",
            "Hand-writing a sort in real projects. Use the built-in unless you're practising.",
        ],
        "Sort first when order would make the problem easier: finding duplicates, merging intervals, two pointers or binary search. Remember it costs O(n log n).",
    ),
    "binary-search": (
        """Think of the \"guess my number from 1 to 100\" game. Nobody sensible guesses 1, 2, 3… You guess 50, hear \"higher\", then guess 75. **Every guess removes half of the remaining possibilities.** That is binary search, and it only works because the numbers are in order.""",
        """Find 23 in `[2, 5, 8, 12, 16, 23, 38]`:

| lo | hi | mid | nums[mid] | Decision |
| --- | --- | --- | --- | --- |
| 0 | 6 | 3 | 12 | Too small, lo = 4 |
| 4 | 6 | 5 | 23 | Found at index 5! |

Two checks, where a linear scan needs six. Doubling the list's size adds only one more check.""",
        [
            "Using it on unsorted data, which gives wrong answers with no error.",
            "Writing `lo = mid` or `hi = mid` with `while lo <= hi`, which can loop forever.",
            "Mixing conventions: choose inclusive `[lo, hi]` or half-open `[lo, hi)` and stay consistent.",
        ],
        "Use it on sorted data, and also for \"find the smallest value that works\" when any larger value would work too.",
    ),
    "trees": (
        """A tree is like a family tree or the folders on your computer: one top item, branching down into children. Each folder holds smaller folders, which is why **most tree solutions are short recursive functions**: solve the left part, solve the right part, combine. A binary search tree adds a rule, smaller values left and larger right, so finding a value is like playing higher-or-lower.""",
        """Depth of this tree, working from the bottom up:

```
      3            depth = 1 + max(1, 2) = 3
     / \\
    9   20         9 has depth 1; 20 has 1 + max(1, 1) = 2
       /  \\
      15   7       leaves have depth 1
```

Traversal order for the same tree: **in-order** gives 9, 3, 15, 20, 7 and **level-order** gives 3, 9, 20, 15, 7.""",
        [
            "Forgetting the `if node is None` check.",
            "Validating a BST by checking only a node's direct children; the rule covers whole subtrees.",
            "Assuming all BSTs are fast. Inserting sorted data makes one a slow, O(n) line.",
        ],
        "Use trees for hierarchical data and sorted data that changes. If a problem gives you a `TreeNode`, start by asking what each node needs from its children.",
    ),
    "tries": (
        """Think of your phone's autocomplete. Type \"ca\" and it instantly suggests \"cat\" and \"car\", because those words **share the path c → a** and then branch. A trie stores words this way, one letter per step, so words with the same beginning share the same path.""",
        """Inserting `car`, then `cat`, then searching:

```
root
 └─ c
     └─ a
         ├─ r  ✓ (word ends)
         └─ t  ✓ (word ends)
```

- `search("cat")`: follow c, a, t. A word ends there, so **True**.
- `search("ca")`: the path exists, but no word ends there, so **False**.
- `starts_with("ca")`: the path exists, so **True**.""",
        [
            "Forgetting the end-of-word marker, which makes \"ca\" look like a stored word.",
            "Using a trie when you only need exact-word checks; a set is simpler.",
            "Rebuilding the trie for every query, instead of building it once.",
        ],
        "Use a trie when a problem is about **prefixes**: autocomplete, \"starts with\", or matching many words at once.",
    ),
    "heaps": (
        """Picture a hospital emergency room: patients aren't seen in arrival order, the most urgent goes next. New patients keep arriving, and you only ever need to know who's most urgent right now. **A heap gives you the next most important item quickly**, without the cost of keeping everything fully sorted.""",
        """Pushing 1 into the min-heap `[2, 5, 3]`:

```
Append at the end:  [2, 5, 3, 1]
1's parent is 5, and 1 is smaller: swap   [2, 1, 3, 5]
1's parent is 2, and 1 is smaller: swap   [1, 2, 3, 5]
1 is at the root: done
```

Only about log n swaps were needed. The list isn't fully sorted, and doesn't need to be: **only the smallest item is guaranteed to be first**.""",
        [
            "Assuming `heap[1]` is the second smallest in order, or that the list is sorted.",
            "Looking for a max-heap in `heapq`. Push negated values instead.",
            "Pushing tuples whose first items tie and whose next items can't be compared. Add a counter as a tie-breaker.",
        ],
        "Use a heap for \"top k\", \"next smallest\", merging sorted lists, or scheduling where new items keep arriving.",
    ),
    "graphs": (
        """A graph is a map of connections: cities joined by roads, or friends on a social network. **BFS** is like ripples in a pond: it reaches everything 1 step away, then 2 steps, and so on. **DFS** is like exploring a maze: follow one path as far as it goes, then back up and try another.""",
        """BFS from A, where A connects to B and C, B connects to D, and C connects to D:

| Visit | Queue afterwards | Seen |
| --- | --- | --- |
| A | B, C | A, B, C |
| B | C, D | A, B, C, D |
| C | D | A, B, C, D |
| D | empty | A, B, C, D |

D is added only once, even with two ways to reach it, thanks to `seen`. A DFS with a stack might instead go A, C, D, B.""",
        [
            "Forgetting `seen`, which makes cycles loop forever.",
            "Marking nodes as seen when popped rather than when added, which lets duplicates pile up.",
            "Using DFS for shortest paths. Use BFS for equal-cost edges.",
        ],
        "Think \"graph\" whenever things connect: grids, dependencies, networks. Use BFS for the fewest steps, and DFS for exploring everything or finding connected groups.",
    ),
    "shortest-paths": (
        """Imagine planning a trip where each road has a different travel time. The route with the fewest roads may not be the fastest. **Dijkstra's algorithm works outward from the start, always settling the closest place not yet settled**, and checks whether going through it creates a quicker route to its neighbours.""",
        """From A, with roads A–B (4), A–C (1) and C–B (2):

| Settle | Distance | What it updates |
| --- | --- | --- |
| A | 0 | B = 4, C = 1 |
| C | 1 | B: 1 + 2 = 3, better than 4, so B = 3 |
| B | 3 | Nothing else |

The direct road to B costs 4, but going through C costs **3**. Choosing the smallest unsettled distance is what guarantees the answer is right.""",
        [
            "Using Dijkstra with negative edge weights. Use Bellman-Ford.",
            "Not skipping stale heap entries, which wastes time.",
            "Reaching for Dijkstra when all edges cost the same; BFS is simpler.",
        ],
        "Use Dijkstra for the cheapest route when edges have different non-negative costs: time, distance, price or effort.",
    ),
    "union-find": (
        """Imagine students forming groups, where each group has a leader. To check if two students are in the same group, ask each for their leader and compare. To merge two groups, one leader simply starts following the other. **Union-Find tracks groups this way**, and it gets faster as it goes, because students learn to point straight at their top leader.""",
        """Five people `0..4`, each starting alone:

| Operation | parent array | Groups |
| --- | --- | --- |
| Start | `[0, 1, 2, 3, 4]` | 5 |
| union(0, 1) | `[0, 0, 2, 3, 4]` | 4 |
| union(3, 4) | `[0, 0, 2, 3, 3]` | 3 |
| union(1, 3) | `[0, 0, 2, 0, 3]` | 2 |

`find(4)` follows 4 → 3 → 0, so 4's leader is 0. Path compression then points 4 directly at 0.""",
        [
            "Comparing `parent[a] == parent[b]` rather than `find(a) == find(b)`.",
            "Merging `a` and `b` themselves, rather than their roots.",
            "Reducing the group count even when both are already in the same group.",
        ],
        "Use it when connections arrive over time and you keep asking \"are these connected?\" or \"how many groups are there?\", and for detecting cycles in undirected graphs.",
    ),
    "greedy": (
        """Say you want to attend as many talks as possible at a conference. A simple rule works: always pick the talk that **finishes earliest**, because that leaves you the most time for the rest. A greedy algorithm follows one simple rule like this at each step and never looks back. The hard part is being sure the rule really gives the best overall result.""",
        """Talks: `[1, 4]`, `[3, 5]`, `[0, 6]`, `[5, 7]`, already sorted by finish time:

| Talk | Starts after the last one ended? | Decision | Busy until |
| --- | --- | --- | --- |
| 1–4 | Yes | Keep | 4 |
| 3–5 | No (3 < 4) | Skip | 4 |
| 0–6 | No (0 < 4) | Skip | 4 |
| 5–7 | Yes (5 ≥ 4) | Keep | 7 |

Two talks is the maximum. Picking the earliest **start** instead would choose 0–6, and no other talk would fit: sometimes the right rule isn't the obvious one.""",
        [
            "Assuming greedy works because it sounds sensible. Try to find a counterexample first.",
            "Sorting by the wrong property, such as start time rather than end time.",
            "Using it when an early choice can ruin later ones; that usually calls for DP.",
        ],
        "Try greedy when a sort plus one pass seems possible, and when you can explain why the local choice never hurts. If you find a counterexample, switch to DP.",
    ),
    "dynamic-programming": (
        """If someone writes `1+1+1+1` and asks for the total, you say 4. Add another `+1` and you instantly say 5, because you **remembered** the last answer instead of recounting. That is dynamic programming: break a problem into smaller ones, save each answer, and build on them instead of solving anything twice.""",
        """Ways to climb 5 stairs, taking 1 or 2 steps at a time. To reach any stair, your last move came from one or two stairs below:

| Stair | Ways | Why |
| --- | --- | --- |
| 1 | 1 | Only one way |
| 2 | 2 | 1+1 or 2 |
| 3 | 3 | ways(2) + ways(1) |
| 4 | 5 | ways(3) + ways(2) |
| 5 | 8 | ways(4) + ways(3) |

Each answer took one addition. Plain recursion recalculates the same stairs repeatedly, and becomes exponentially slower as n grows.""",
        [
            "Starting to code before stating what `dp[i]` means in words.",
            "Wrong base cases or table sizes. Tables often need `n + 1` entries.",
            "Filling the table in an order where needed values aren't ready yet.",
        ],
        "Think DP when a problem asks for the **best**, the **number of ways**, or **is it possible**, and choices at each step lead to repeated smaller problems.",
    ),
}


def build_lesson(topic_id: str, lesson: str) -> str:
    intro, walkthrough, mistakes, when = GUIDES[topic_id]
    mistake_list = "\n".join(f"- {item}" for item in mistakes)
    return f"""
## The big idea

{intro}
{lesson.rstrip()}

## Worked example, step by step

{walkthrough}

## Common mistakes

{mistake_list}

## When to use it

{when}
"""
