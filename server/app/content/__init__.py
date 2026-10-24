"""Study content: one module per topic, in learning order."""

from . import (
    arrays,
    big_o,
    binary_search,
    dynamic_programming,
    graphs,
    hashing,
    heaps,
    linked_lists,
    recursion,
    sorting,
    stacks_queues,
    trees,
)

TOPICS = [
    module.TOPIC
    for module in (
        big_o,
        arrays,
        hashing,
        linked_lists,
        stacks_queues,
        recursion,
        sorting,
        binary_search,
        trees,
        heaps,
        graphs,
        dynamic_programming,
    )
]

TOPICS_BY_ID = {topic["id"]: topic for topic in TOPICS}

for topic in TOPICS:
    for problem in topic["problems"]:
        problem["topic"] = topic["id"]

PROBLEMS = [problem for topic in TOPICS for problem in topic["problems"]]

PROBLEMS_BY_ID = {problem["id"]: problem for problem in PROBLEMS}
