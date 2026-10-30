"""Check that the study content is well-formed and every reference solution passes."""

import importlib.util
import json
from pathlib import Path

import pytest

from app.content import PROBLEMS, TOPICS

HARNESS_PATH = Path(__file__).resolve().parents[2] / "src" / "python" / "harness.py"
spec = importlib.util.spec_from_file_location("harness", HARNESS_PATH)
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


def run(code, problem):
    return json.loads(harness.run_tests(code, json.dumps(problem)))


def test_ids_are_unique():
    assert len({t["id"] for t in TOPICS}) == len(TOPICS)
    assert len({p["id"] for p in PROBLEMS}) == len(PROBLEMS)


def _ints(value):
    if isinstance(value, bool):
        return
    if isinstance(value, int):
        yield value
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from _ints(item)


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_values_survive_javascript(problem):
    """Browsers parse test data as JS numbers, which are exact only up to 2**53."""
    for test in problem["tests"]:
        for value in _ints([test["args"], test["expected"]]):
            assert abs(value) <= 2**53, value


@pytest.mark.parametrize("topic", TOPICS, ids=lambda t: t["id"])
def test_topic_shape(topic):
    for key in ("title", "category", "summary", "visualizer", "lesson", "complexity", "snippets"):
        assert topic[key], key
    assert topic["problems"]
    for item in topic["quiz"]:
        assert 0 <= item["answer"] < len(item["options"])
        assert item["explanation"]
    assert len(topic["flashcards"]) >= 5
    for card in topic["flashcards"]:
        assert card["front"] and card["back"]


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_reference_solution_passes(problem):
    outcome = run(problem["solution"], problem)
    assert outcome["error"] is None
    failures = [r for r in outcome["results"] if not r["passed"]]
    assert not failures, failures


@pytest.mark.parametrize("problem", PROBLEMS, ids=lambda p: p["id"])
def test_starter_code_runs_but_fails(problem):
    outcome = run(problem["starter"], problem)
    assert outcome["error"] is None
    assert not all(r["passed"] for r in outcome["results"])


@pytest.mark.parametrize("topic", TOPICS, ids=lambda t: t["id"])
def test_snippets_run(topic):
    for snippet in topic["snippets"]:
        assert json.loads(harness.run_code(snippet["code"]))["error"] is None, snippet["title"]


def test_harness_reports_errors():
    problem = PROBLEMS[0]
    assert "SyntaxError" in run("def oops(:\n", problem)["error"]
    assert "Define" in run("x = 1\n", problem)["error"]


def test_leetcode_links_point_at_real_problems():
    from app.content.leetcode import LEETCODE_SLUGS

    known = {p["id"] for p in PROBLEMS}
    assert set(LEETCODE_SLUGS) <= known
