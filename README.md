# Algorithm Visualizer

An interactive, full-stack app for learning sorting algorithms through step-by-step visualizations.

## Features

- Animated Bubble, Selection, Insertion, Merge and Quick Sort
- Play, pause, step forward/back, and adjustable speed
- Live comparison and swap counters
- Time/space complexity and stability for each algorithm (served by the API)
- Accounts (sign up / log in) with saved run history and per-algorithm stats

## Tech Stack

- **Frontend:** React 19, Vite, CSS
- **Backend:** Express 5 (TypeScript via `tsx`), JWT auth, bcrypt
- **Database:** PostgreSQL with Prisma 7

## Project Structure

```
src/                  React app
  components/         UI components
  utils/sorting.js    Step generators for each algorithm
  api.js              Fetch helper (adds the auth token)
server/
  src/index.ts        Express app entry
  src/auth.ts         /api/auth routes + requireAuth middleware
  src/sessions.ts     /api/sessions routes (saved runs)
  src/algorithms.ts   Algorithm metadata
  src/prisma/         Prisma schema
  prisma/migrations/  Database migrations
```

## Getting Started

Requires Node 22+ and PostgreSQL 15+.

```bash
# 1. Install dependencies
npm install
npm --prefix server install

# 2. Configure the server
cp server/.env.example server/.env   # then fill in DATABASE_URL and JWT_SECRET

# 3. Create the database tables
cd server && npx prisma migrate dev && cd ..

# 4. Run the API and the frontend (two terminals)
npm run dev:server
npm run dev
```

Open http://localhost:5173. Vite proxies `/api` requests to the API on port 5001.

For production, `npm start` builds the frontend and serves it from the Express server.

## API

| Method | Route                | Auth | Description                     |
| ------ | -------------------- | ---- | ------------------------------- |
| GET    | `/api/health`        |      | Health check                    |
| GET    | `/api/algorithms`    |      | Algorithm metadata              |
| POST   | `/api/auth/register` |      | Create an account               |
| POST   | `/api/auth/login`    |      | Log in, returns a JWT           |
| GET    | `/api/auth/me`       | ✓    | Current user                    |
| GET    | `/api/sessions`      | ✓    | Recent runs + per-algorithm stats |
| POST   | `/api/sessions`      | ✓    | Save a run                      |
| DELETE | `/api/sessions/:id`  | ✓    | Delete a run                    |

## Roadmap

- Binary Search Tree operations
- N-Queens backtracking
- Predict Mode: guess the next step
- Race Mode: run algorithms side by side
