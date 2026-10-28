def test_health(client):
    assert client.get("/api/health").json()["success"] is True


def test_topics_and_problems(client):
    topics = client.get("/api/topics").json()["topics"]
    assert len(topics) == 18

    topic = client.get("/api/topics/arrays").json()["topic"]
    assert topic["problems"][0]["id"] == "pair-sum-sorted"

    problem = client.get("/api/problems/two-sum").json()["problem"]
    assert problem["function"] == "two_sum"

    assert client.get("/api/topics/nope").status_code == 404
    assert client.get("/api/problems/nope").json() == {"error": "Problem not found."}


def test_register_login_me(client):
    body = {"email": "Ada@Example.com", "username": "ada", "password": "password123"}
    assert client.post("/api/auth/register", json=body).status_code == 201
    assert client.post("/api/auth/register", json=body).status_code == 409

    bad = client.post("/api/auth/login", json={"email": "ada@example.com", "password": "nope"})
    assert bad.status_code == 401

    token = client.post(
        "/api/auth/login", json={"email": "ada@example.com", "password": "password123"}
    ).json()["token"]
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.json()["user"]["username"] == "ada"


def test_register_validation(client):
    response = client.post(
        "/api/auth/register", json={"email": "x@y.z", "username": "a", "password": "password123"}
    )
    assert response.status_code == 400
    assert "Username" in response.json()["error"]


def test_quiz_hides_answers_and_grades(client, auth_headers):
    questions = client.get("/api/topics/big-o/quiz").json()["questions"]
    assert "answer" not in questions[0]

    result = client.post(
        "/api/topics/big-o/quiz", json={"answers": [2, 1, 3, 1, 0]}, headers=auth_headers
    ).json()
    assert result["score"] == 5

    progress = client.get("/api/progress", headers=auth_headers).json()
    assert progress["quizBest"]["big-o"] == {"score": 5, "total": 5}


def test_quiz_works_without_login(client):
    result = client.post("/api/topics/big-o/quiz", json={"answers": [None] * 5}).json()
    assert result["score"] == 0


def test_progress_requires_login(client):
    assert client.get("/api/progress").status_code == 401


def test_topic_and_problem_progress(client, auth_headers):
    assert client.put("/api/progress/topics/arrays", headers=auth_headers).status_code == 204
    assert client.put("/api/progress/topics/arrays", headers=auth_headers).status_code == 204

    client.put("/api/problems/two-sum/progress", json={"code": "x", "passed": False},
               headers=auth_headers)
    saved = client.put("/api/problems/two-sum/progress", json={"code": "y", "passed": True},
                       headers=auth_headers).json()
    assert saved == {"solved": True, "attempts": 2}

    state = client.get("/api/problems/two-sum/progress", headers=auth_headers).json()
    assert state["code"] == "y"

    progress = client.get("/api/progress", headers=auth_headers).json()
    assert progress["completedTopics"] == ["arrays"]
    assert progress["solvedProblems"] == ["two-sum"]

    client.delete("/api/progress/topics/arrays", headers=auth_headers)
    assert client.get("/api/progress", headers=auth_headers).json()["completedTopics"] == []


def test_flashcards_are_public(client):
    cards = client.get("/api/flashcards?topic=heaps").json()["cards"]
    assert cards[0]["id"] == "heaps:0"
    assert client.get("/api/flashcards?topic=nope").status_code == 404


def test_review_moves_cards_between_boxes(client, auth_headers):
    queue = client.get("/api/review?topic=heaps", headers=auth_headers).json()
    assert queue["due"] == [] and len(queue["new"]) == 5

    assert client.post("/api/review/heaps:0", json={"correct": True}, headers=auth_headers).json()["box"] == 1
    assert client.post("/api/review/heaps:0", json={"correct": True}, headers=auth_headers).json()["box"] == 2
    assert client.post("/api/review/heaps:0", json={"correct": False}, headers=auth_headers).json()["box"] == 1

    queue = client.get("/api/review?topic=heaps", headers=auth_headers).json()
    assert len(queue["new"]) == 4
    assert queue["stats"]["seen"] == 1 and queue["stats"]["boxes"][0] == 1

    assert client.post("/api/review/nope:1", json={"correct": True}, headers=auth_headers).status_code == 404
    assert client.get("/api/review").status_code == 401
