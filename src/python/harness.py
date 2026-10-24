"""Test harness for practice problems.

Runs in the browser through Pyodide, and in the backend test suite to check
that every reference solution passes its own tests.
"""

import contextlib
import copy
import io
import json
import traceback


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        return f"ListNode({self.val})"


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val})"


def build_list(values):
    dummy = ListNode()
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def list_values(node):
    values = []
    while node is not None and len(values) < 10_000:
        values.append(node.val)
        node = node.next
    return values


def build_tree(values):
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    return root


def tree_values(root):
    values = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            values.append(None)
            continue
        values.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while values and values[-1] is None:
        values.pop()
    return values


TO_PYTHON = {"linked_list": build_list, "tree": build_tree}
FROM_PYTHON = {"linked_list": list_values, "tree": tree_values}


def to_json_value(value):
    """Round-trip through JSON so tuples become lists, matching expected values."""
    return json.loads(json.dumps(value, default=repr))


def normalize(value, compare):
    if compare == "unordered":
        return sorted(value, key=repr)
    if compare == "unordered_nested":
        return sorted((sorted(item, key=repr) for item in value), key=repr)
    if compare == "float":
        return round(value, 5)
    return value


def short_traceback():
    lines = traceback.format_exc().strip().splitlines()
    # Drop the harness frames so learners only see their own code.
    keep = [line for line in lines if "harness" not in line]
    return "\n".join(keep[-6:])


def run_design(cls, test):
    instance = None
    outputs = []
    for op, args in zip(test["ops"], test["args"]):
        if instance is None:
            instance = cls(*args)
            outputs.append(None)
        else:
            outputs.append(getattr(instance, op)(*args))
    return outputs


def run_case(target, problem, test):
    if problem.get("mode") == "design":
        return run_design(target, test)

    arg_types = problem.get("arg_types") or [None] * len(test["args"])
    args = [
        TO_PYTHON[kind](copy.deepcopy(arg)) if kind else copy.deepcopy(arg)
        for arg, kind in zip(test["args"], arg_types)
    ]
    result = target(*args)

    if problem.get("inplace") is not None:
        result = args[problem["inplace"]]
    if problem.get("return_type"):
        result = FROM_PYTHON[problem["return_type"]](result)
    return result


def run_tests(code, problem_json):
    problem = json.loads(problem_json)
    compare = problem.get("compare", "exact")
    namespace = {"ListNode": ListNode, "TreeNode": TreeNode, "__name__": "solution"}
    setup_output = io.StringIO()

    try:
        with contextlib.redirect_stdout(setup_output):
            exec(compile(code, "solution.py", "exec"), namespace)
    except Exception:
        return json.dumps({"error": short_traceback(), "results": []})

    target = namespace.get(problem["function"])
    if target is None:
        return json.dumps(
            {"error": f"Define `{problem['function']}` in your code.", "results": []}
        )

    results = []
    for test in problem["tests"]:
        output = io.StringIO()
        if "ops" in test:
            shown_input = [[op, *args] for op, args in zip(test["ops"], test["args"])]
        else:
            shown_input = test["args"]
        entry = {"input": shown_input, "expected": test["expected"]}
        try:
            with contextlib.redirect_stdout(output):
                got = to_json_value(run_case(target, problem, test))
            entry["got"] = got
            entry["passed"] = normalize(got, compare) == normalize(test["expected"], compare)
        except Exception:
            entry["passed"] = False
            entry["error"] = short_traceback()
        entry["stdout"] = output.getvalue()[-2000:]
        results.append(to_json_value(entry))

    return json.dumps({"error": None, "results": results})


def run_code(code):
    output = io.StringIO()
    error = None
    try:
        with contextlib.redirect_stdout(output):
            exec(compile(code, "main.py", "exec"), {"__name__": "__main__"})
    except Exception:
        error = short_traceback()
    return json.dumps({"stdout": output.getvalue()[-20_000:], "error": error})
