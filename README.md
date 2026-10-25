# DSA Study Lab

A full-stack app for learning data structures and algorithms in Python: short lessons, step-by-step visualizers that highlight the running line of Python, practice problems you solve in the browser, and quizzes, with progress saved to your account.

## Features

- **12 topics**: Big-O, arrays & two pointers, hash maps, linked lists, stacks & queues, recursion & backtracking, sorting, binary search, trees & BSTs, heaps, graphs (BFS/DFS) and dynamic programming
- **Interactive visualizers** for every topic, with play/pause/step controls, live variables and Python line highlighting
- **37 practice problems** with hints and reference solutions; your code runs against test cases in the browser via [Pyodide](https://pyodide.org)
- **Python playground** for free experimentation
- **Quizzes** graded by the server, with explanations
- **Progress dashboard**: completed topics, solved problems, best quiz scores

## Tech stack

- **Frontend:** React 19, React Router, Vite, CodeMirror, Pyodide (in a Web Worker)
- **Backend:** Python, FastAPI, SQLAlchemy, Alembic, JWT auth with bcrypt
- **Database:** PostgreSQL
- **Tests:** pytest (API tests, plus every reference solution is run against its own test cases)

## Project structure

```
src/
  pages/          Home, Topic, Problems, Problem, Playground, Dashboard
  components/     Navbar, CodeEditor, Quiz, TestResults, ...
  visualizers/    One component per topic + shared player/layout
  python/         harness.py (test runner), Pyodide worker and runner
server/
  app/main.py     FastAPI app
  app/routers/    auth, content, progress
  app/content/    Lessons, problems and quizzes (one module per topic)
  migrations/     Alembic migrations
  tests/          pytest suite
```

## Getting started

Requires Node 22+, Python 3.12+ and PostgreSQL.

```bash
# Frontend dependencies
npm install

# Backend: virtualenv, dependencies and config
cd server
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
cp .env.example .env          # fill in DATABASE_URL and JWT_SECRET
.venv/bin/alembic upgrade head
cd ..

# Run (two terminals)
npm run dev:server            # API on http://localhost:8000
npm run dev                   # app on http://localhost:5173
```

Run the backend tests with `npm run test:server`. For production, `npm start` builds the frontend and serves it from FastAPI.

## API

| Method | Route | Auth | Description |
| --- | --- | --- | --- |
| GET | `/api/topics` | | List topics |
| GET | `/api/topics/{id}` | | Lesson, snippets, complexity and problems |
| GET / POST | `/api/topics/{id}/quiz` | optional | Get questions / submit answers |
| GET | `/api/problems` · `/api/problems/{id}` | | Problems |
| POST | `/api/auth/register` · `/api/auth/login` | | Get a JWT |
| GET | `/api/auth/me` | ✓ | Current user |
| GET | `/api/progress` | ✓ | Dashboard data |
| PUT / DELETE | `/api/progress/topics/{id}` | ✓ | Mark a topic complete / incomplete |
| GET / PUT | `/api/problems/{id}/progress` | ✓ | Saved code and solved status |
