"""Study content: one module per topic, in learning order."""

from . import (
    arrays,
    big_o,
    binary_search,
    bit_manipulation,
    dynamic_programming,
    graphs,
    greedy,
    hashing,
    heaps,
    linked_lists,
    recursion,
    shortest_paths,
    sliding_window,
    sorting,
    stacks_queues,
    trees,
    tries,
    union_find,
)
from .leetcode import LEETCODE_SLUGS

TOPICS = [
    module.TOPIC
    for module in (
        big_o,
        bit_manipulation,
        arrays,
        sliding_window,
        hashing,
        linked_lists,
        stacks_queues,
        recursion,
        sorting,
        binary_search,
        trees,
        tries,
        heaps,
        graphs,
        shortest_paths,
        union_find,
        greedy,
        dynamic_programming,
    )
]

TOPICS_BY_ID = {topic["id"]: topic for topic in TOPICS}

for topic in TOPICS:
    for problem in topic["problems"]:
        problem["topic"] = topic["id"]
        problem["leetcode"] = LEETCODE_SLUGS.get(problem["id"])

PROBLEMS = [problem for topic in TOPICS for problem in topic["problems"]]

PROBLEMS_BY_ID = {problem["id"]: problem for problem in PROBLEMS}

# Card ids are "<topic>:<index>", stable as long as cards are only appended.
CARDS = [
    {"id": f"{topic['id']}:{i}", "topic": topic["id"], **card}
    for topic in TOPICS
    for i, card in enumerate(topic["flashcards"])
]

CARDS_BY_ID = {card["id"]: card for card in CARDS}
