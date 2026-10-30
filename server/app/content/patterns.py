"""'Which technique fits this problem?' questions."""

TECHNIQUES = [
    "Two pointers", "Sliding window", "Hash map", "Binary search", "Stack",
    "BFS", "DFS / backtracking", "Heap", "Dynamic programming", "Greedy", "Union-Find", "Trie",
]

PATTERNS = [
    ("Find two numbers in a sorted array that add up to a target, using O(1) extra space.", "Two pointers", "Sorted order lets you move inward from both ends, discarding one candidate per step."),
    ("Find the longest substring containing at most two distinct characters.", "Sliding window", "A contiguous range with a rule that can be restored by shrinking from the left."),
    ("Check whether any two values in an unsorted list sum to a target, in O(n) time.", "Hash map", "Look up each number's complement in O(1)."),
    ("Find the smallest ship capacity that delivers all packages within D days.", "Binary search", "Feasibility is monotonic in capacity, so search on the answer."),
    ("For each day, find how many days until a warmer temperature.", "Stack", "A monotonic stack holds days still waiting for a warmer one."),
    ("Find the fewest moves for a knight to reach a square on a chessboard.", "BFS", "Every move costs the same, so BFS finds the shortest path."),
    ("Generate all valid arrangements of n parentheses pairs.", "DFS / backtracking", "Build each answer choice by choice and undo to explore the others."),
    ("Keep track of the 10 largest scores in a very long stream.", "Heap", "A min-heap of size k keeps the top k in O(n log k)."),
    ("Count the ways to make change for an amount using given coins.", "Dynamic programming", "Overlapping subproblems: ways(amount) builds on smaller amounts."),
    ("Attend the maximum number of non-overlapping talks.", "Greedy", "Always taking the talk that ends earliest is provably optimal."),
    ("Given friendships arriving one at a time, report how many friend groups exist after each.", "Union-Find", "Merging groups incrementally is exactly what DSU does."),
    ("Suggest all dictionary words as a user types each letter.", "Trie", "Words sharing a prefix share a path, so prefix lookups are direct."),
    ("Find the first and last position of a value in a sorted array in O(log n).", "Binary search", "Run two boundary searches on the sorted data."),
    ("Find the shortest subarray whose sum is at least a target (all positive numbers).", "Sliding window", "With positive numbers, growing raises the sum and shrinking lowers it."),
    ("Remove duplicates from a sorted array in place.", "Two pointers", "A slow pointer marks the next slot while a fast one scans."),
    ("Find the maximum sum of non-adjacent houses to rob.", "Dynamic programming", "Each house's best depends on the best from one and two houses back."),
]
