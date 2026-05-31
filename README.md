# CodeRank

An online judge platform for competitive programming. Users solve algorithmic problems, submit solutions in multiple languages, and compete on a global leaderboard. Code runs inside sandboxed Docker containers and results stream back in real time over WebSockets.

---

## Key Features

- JWT Authentication & Role-Based Access Control (User / Moderator / Admin)
- Real-Time Submission Status Updates using WebSockets
- Docker-Based Secure Code Execution Sandbox
- Asynchronous Processing using Celery + Redis
- Leaderboard with First-Solve Scoring
- Multi-Language Support
- Prometheus Metrics Integration
- Automated Test Suite (23 Tests, 72% Coverage)
- Sandbox Isolation Verification

---

## Supported Languages

Currently Supported:

| Language | Version |
|---|---|
| Python | 3.12 |
| JavaScript | Node.js 20 |

The platform is designed to support additional languages through configuration in the `languages` table without requiring architecture changes.

---

## Frontend

Frontend Stack:

- React
- Vite
- Axios
- Context API
- WebSockets

Implemented Screens:

- Login / Registration
- Problems List
- Problem Detail
- Online Code Editor
- Submission History
- Leaderboard
- User Profile
- Admin Management Screens

---

## Table of Contents

- [Key Features](#key-features)
- [Supported Languages](#supported-languages)
- [Frontend](#frontend)
- [Architecture](#architecture)
- [Setup Guide](#setup-guide)
- [Seed Demo Data](#seed-demo-data)
- [API Documentation](#api-documentation)
- [Database Design](#database-design)
- [Execution Flow](#execution-flow)
- [Test Results](#test-results)
- [Sandbox Validation](#sandbox-validation)
- [Security Design](#security-design)
- [Demo Walkthrough](#demo-walkthrough)
- [Future Enhancements](#future-enhancements)
- [Project Status](#project-status)

---

## Architecture

### High-Level Overview

```
                           ┌──────────────────────────────────────────────┐
                           │              Docker Compose                  │
                           │                                              │
┌──────────┐    HTTP/WS    │  ┌───────────┐       ┌──────────────────┐   │
│          │◄─────────────►│  │  FastAPI   │◄─────►│   PostgreSQL 16  │   │
│  Client  │               │  │   :8000    │  SQL  │     :5432        │   │
│          │               │  └─────┬─────┘       └──────────────────┘   │
└──────────┘               │        │                                     │
                           │        │ enqueue                             │
                           │        ▼                                     │
                           │  ┌───────────┐       ┌──────────────────┐   │
                           │  │   Redis    │◄─────►│  Celery Worker   │   │
                           │  │   :6379    │ poll  │                  │   │
                           │  └───────────┘       └────────┬─────────┘   │
                           │                               │              │
                           │                               │ spawn        │
                           │                               ▼              │
                           │                      ┌──────────────────┐   │
                           │                      │ Docker Sandbox   │   │
                           │                      │ (per execution)  │   │
                           │                      └──────────────────┘   │
                           └──────────────────────────────────────────────┘
```

### Components

| Component | Role |
|---|---|
| **FastAPI** | Async HTTP API server. Handles all REST endpoints, request validation (Pydantic), JWT auth, and WebSocket connections. |
| **PostgreSQL 16** | Primary data store. Holds users, problems, test cases, submissions, execution results, and leaderboard rankings. Accessed via async SQLAlchemy. |
| **Redis 7** | Celery message broker and result backend. Queues execution tasks for workers. |
| **Celery Worker** | Consumes tasks from the `execution_queue`. Orchestrates code execution, verdict classification, leaderboard updates, and WebSocket status broadcasts. Auto-retries on failure (up to 3 retries, exponential backoff). |
| **Docker Sandbox** | Ephemeral containers spawned per code execution. Runs user code with network disabled, 128 MB memory cap, and 0.5 CPU limit. Destroyed immediately after execution. |

### Layered Application Structure

```
app/
├── api/            →  Route handlers & dependency injection
├── schemas/        →  Pydantic request/response models
├── services/       →  Business logic
├── repositories/   →  Database queries (SQLAlchemy)
├── models/         →  ORM table definitions
├── workers/        →  Celery background tasks
├── sandbox/        →  Docker runner & verdict classifier
├── middleware/     →  Rate limiting and request processing
├── core/           →  Config, DB engine, security, logging, metrics
└── utils/          →  Shared helpers & constants
```

---

## Setup Guide

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.12+ *(only for local development without Docker)*

### 1. Clone & Configure

```bash
git clone https://github.com/Amoghk3/coderank.git
cd coderank
cp .env.example .env
```

Edit `.env`:

```env
APP_NAME=CodeRank

POSTGRES_USER=coderank
POSTGRES_PASSWORD=coderank
POSTGRES_DB=coderank

DATABASE_URL=postgresql+asyncpg://coderank:coderank@postgres:5432/coderank

REDIS_URL=redis://redis:6379/0

SECRET_KEY=<generate-a-strong-random-key>

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 2. Start Services

```bash
docker compose up --build
```

This brings up four containers:

| Container | Service | Port |
|---|---|---|
| `coderank_api` | FastAPI + Uvicorn (hot-reload) | `8000` |
| `coderank_postgres` | PostgreSQL 16 | `5432` |
| `coderank_redis` | Redis 7 Alpine | `6379` |
| `coderank_worker` | Celery worker | — |

### 3. Run Migrations

```bash
docker compose exec api alembic upgrade head
```

### 4. Seed Demo Data

```bash
docker compose exec api python scripts/seed_data.py
```

### 5. Verify

```bash
curl http://localhost:8000/health
# → {"status": "ok"}
```

Interactive Swagger docs are available at **http://localhost:8000/docs**.

### Local Development (without Docker Compose)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start API server
uvicorn app.main:app --reload --port 8000

# Start Celery worker (separate terminal)
celery -A app.workers.celery_app worker --loglevel=info
```

> **Note:** Requires a running PostgreSQL and Redis instance. Update `DATABASE_URL` and `REDIS_URL` in `.env` to point at your local instances.

---

## Seed Demo Data

Run:

```bash
docker compose exec api python scripts/seed_data.py
```

Creates:

### Users

| Role | Email | Password |
|---|---|---|
| Admin | `admin@test.com` | `Admin123!` |
| User | `user@test.com` | `User123!` |

### Languages

- Python 3.12
- JavaScript (Node.js 20)

### Problems

- Two Sum
- Palindrome Number
- Valid Parentheses
- Longest Substring Without Repeating Characters
- Merge Intervals

### Test Cases

15 test cases across 5 problems (3 per problem — 2 visible + 1 hidden).

The script is idempotent — running it multiple times will skip existing records.

---

## API Documentation

Base URL: `/api/v1`

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/auth/register` | — | Register a new user |
| `POST` | `/auth/login` | — | Login (returns JWT) |
| `GET` | `/auth/me` | Bearer | Get current user profile |
| `POST` | `/auth/logout` | Bearer | Logout |

**Register**

```
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "coder",
  "password": "strongpassword"
}
```

**Login** — Uses OAuth2 password form:

```
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=strongpassword
```

Returns:

```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer"
}
```

---

### Users

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `PATCH` | `/users/{user_id}/role` | Admin | Update a user's role |

---

### Problems

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/problems` | Admin / Moderator | Create a problem |
| `GET` | `/problems` | — | List all problems |
| `GET` | `/problems/search` | — | Search by difficulty, tag, or keyword |
| `GET` | `/problems/{problem_id}` | — | Get a single problem |
| `PUT` | `/problems/{problem_id}` | Admin / Moderator | Update a problem |
| `DELETE` | `/problems/{problem_id}` | Admin | Delete a problem |

**Create Problem**

```json
{
  "title": "Two Sum",
  "slug": "two-sum",
  "difficulty": "EASY",
  "statement": "Given an array of integers...",
  "input_format": "First line contains n...",
  "output_format": "Print the two indices...",
  "constraints": "2 <= n <= 10^4",
  "sample_input": "4\n2 7 11 15\n9",
  "sample_output": "0 1",
  "time_limit_ms": 2000,
  "memory_limit_mb": 128
}
```

---

### Submissions

| Method | Endpoint | Auth | Rate Limit | Description |
|---|---|---|---|---|
| `POST` | `/submissions/execute` | Bearer | 20/min | Run code against sample test cases |
| `POST` | `/submissions/judge` | Bearer | 5/min | Judge code against all test cases (hidden + public) |
| `GET` | `/submissions/history` | Bearer | — | Get current user's submission history |
| `GET` | `/submissions/{submission_id}` | Bearer | — | Get submission detail |
| `GET` | `/submissions/{submission_id}/results` | Bearer | — | Get execution & judge results |

**Execute Submission**

```json
{
  "problem_id": "uuid",
  "language_id": "uuid",
  "source_code": "print(input())",
  "custom_input": "hello"
}
```

**Judge Submission**

```json
{
  "problem_id": "uuid",
  "language_id": "uuid",
  "source_code": "print(input())"
}
```

---

### Languages

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/languages` | Admin | Add a language |
| `GET` | `/languages` | Bearer | List all languages |
| `GET` | `/languages/{language_id}` | Bearer | Get language detail |
| `PUT` | `/languages/{language_id}` | Admin | Update a language |
| `DELETE` | `/languages/{language_id}` | Admin | Delete a language |

---

### Test Cases

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/problems/{problem_id}/test-cases` | Admin | Create a test case |
| `GET` | `/problems/{problem_id}/test-cases` | Bearer | List test cases for a problem |
| `GET` | `/test-cases/{test_case_id}` | Bearer | Get a single test case |
| `PUT` | `/test-cases/{test_case_id}` | Admin | Update a test case |
| `DELETE` | `/test-cases/{test_case_id}` | Admin | Delete a test case |

---

### Leaderboard

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/leaderboard` | — | Top 100 users ranked by total score, accepted count, and best runtime |

Response:

```json
[
  {
    "rank": 1,
    "user_id": "uuid",
    "email": "user@example.com",
    "accepted_count": 42,
    "total_submissions": 100,
    "total_score": 4200,
    "best_runtime_ms": 45,
    "updated_at": "2026-05-31T12:00:00Z"
  }
]
```

---

### WebSocket

```
ws://localhost:8000/api/v1/ws/submissions/{submission_id}
```

Receives real-time JSON updates as the submission is processed:

```json
{"status": "RUNNING"}
```

```json
{"status": "ACCEPTED", "runtime_ms": 120, "memory_kb": 2048}
```

---

## Database Design

### ER Diagram

```mermaid
erDiagram
    users ||--o{ submissions : submits
    users ||--o| leaderboards : "has ranking"
    users ||--o{ refresh_tokens : "has tokens"
    users ||--o{ solved_problems : "has solved"

    problems ||--o{ submissions : "receives"
    problems ||--o{ test_cases : "has"
    problems ||--o{ problem_tags : "tagged with"
    problems ||--o{ solved_problems : "solved in"

    submissions ||--o{ execution_results : "produces"
    submissions ||--o{ judge_case_results : "judged by"
    submissions ||--o| execution_jobs : "triggers"
    submissions ||--o{ solved_problems : "first solve"

    test_cases ||--o{ judge_case_results : "evaluated in"

    users {
        UUID id PK
        VARCHAR email UK
        VARCHAR username UK
        VARCHAR password_hash
        BOOLEAN is_active
        ENUM role
    }

    problems {
        UUID id PK
        VARCHAR title UK
        VARCHAR slug UK
        ENUM difficulty
        TEXT statement
        TEXT input_format
        TEXT output_format
        TEXT constraints
        TEXT sample_input
        TEXT sample_output
        INT time_limit_ms
        INT memory_limit_mb
        TEXT examples
        TIMESTAMPTZ created_at
    }

    submissions {
        UUID id PK
        UUID user_id FK
        UUID problem_id FK
        UUID language_id FK
        TEXT source_code
        TEXT custom_input
        ENUM status
        INT runtime_ms
        INT memory_kb
        BOOLEAN is_judge
        TIMESTAMPTZ created_at
    }

    languages {
        UUID id PK
        VARCHAR name UK
        VARCHAR version
        VARCHAR docker_image
        VARCHAR compile_command
        VARCHAR run_command
        INT time_limit
        INT memory_limit
        BOOLEAN is_active
    }

    test_cases {
        UUID id PK
        UUID problem_id FK
        TEXT input_data
        TEXT expected_output
        BOOLEAN is_hidden
        INT points
    }

    execution_jobs {
        UUID id PK
        UUID submission_id FK
        TEXT celery_task_id
        ENUM status
        INT retry_count
        TEXT error_message
        TIMESTAMPTZ started_at
        TIMESTAMPTZ completed_at
        TIMESTAMPTZ created_at
    }

    execution_results {
        UUID id PK
        UUID submission_id FK
        TEXT stdout
        TEXT stderr
        TIMESTAMPTZ created_at
    }

    judge_case_results {
        UUID id PK
        UUID submission_id FK
        UUID test_case_id FK
        TEXT expected_output
        TEXT actual_output
        BOOLEAN passed
    }

    leaderboards {
        UUID id PK
        UUID user_id FK
        INT accepted_count
        INT total_submissions
        INT total_score
        INT best_runtime_ms
        TIMESTAMPTZ updated_at
    }

    solved_problems {
        UUID id PK
        UUID user_id FK
        UUID problem_id FK
        UUID first_submission_id FK
        TIMESTAMPTZ solved_at
    }

    refresh_tokens {
        UUID id PK
        UUID user_id FK
        VARCHAR token UK
        BOOLEAN is_revoked
        TIMESTAMPTZ created_at
    }

    problem_tags {
        UUID id PK
        UUID problem_id FK
        VARCHAR tag
    }
```

### Key Design Decisions

- **UUIDs everywhere** — All primary keys are `UUID v4` to avoid sequential ID enumeration.
- **`is_judge` flag on submissions** — A single `submissions` table handles both "run with custom input" (`is_judge=false`) and "judge against all test cases" (`is_judge=true`).
- **Hidden test cases** — `test_cases.is_hidden` separates sample cases (shown to users) from hidden cases (used only during judging).
- **Solved problems deduplication** — `solved_problems` has a `UNIQUE(user_id, problem_id)` constraint. Only the first accepted submission counts toward leaderboard score.
- **Leaderboard materialization** — `leaderboards` is a per-user aggregate table updated in real time during execution, avoiding expensive queries on every leaderboard request.
- **Cascade deletes** — Foreign keys on `execution_jobs`, `execution_results`, `judge_case_results`, `solved_problems`, and `problem_tags` use `ON DELETE CASCADE`.
- **Migrations** — Schema is managed by Alembic with the connection string in `alembic.ini`.

---

## Execution Flow

### Execute (Run with Custom Input)

```
User submits code
       │
       ▼
┌──────────────┐
│  POST        │   1. Validate problem_id and language_id exist
│  /submissions│   2. Create Submission (status=PENDING, is_judge=false)
│  /execute    │   3. Create ExecutionJob (status=QUEUED)
└──────┬───────┘   4. Dispatch Celery task → execute_submission_task.delay(job_id)
       │           5. Return submission to client immediately
       │
       ▼
┌──────────────┐
│ Celery       │   6. Load ExecutionJob + Submission from DB
│ Worker       │   7. Set status → RUNNING, broadcast via WebSocket
│              │   8. Fetch VISIBLE test cases only (is_hidden=false)
│              │   9. For each test case:
│              │       a. Spawn Docker container (network=none, mem=128m, cpu=0.5)
│              │       b. Write source code to temp file, pass stdin
│              │       c. Capture stdout, stderr, exit_code, timeout
│              │       d. Save ExecutionResult
│              │       e. Compare output → save JudgeCaseResult
│              │       f. On timeout → TLE, on crash → RUNTIME_ERROR (break)
│              │  10. Classify final verdict (ACCEPTED / WRONG_ANSWER)
└──────┬───────┘  11. Broadcast final status via WebSocket
       │
       ▼
  Client receives real-time updates via WebSocket
```

### Judge (Official Submission)

```
User submits code
       │
       ▼
┌──────────────┐
│  POST        │   Same steps 1–5 as Execute, but:
│  /submissions│     • is_judge = true
│  /judge      │     • Rate-limited to 5/minute
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Celery       │   Same steps 6–9, but:
│ Worker       │     • Fetches ALL test cases (hidden + visible)
│              │     • On ACCEPTED verdict:
│              │         - Increment leaderboard.total_submissions
│              │         - If first solve: +100 score, record in solved_problems
│              │         - Update best_runtime_ms if improved
└──────┬───────┘     • Broadcast final result via WebSocket
       │
       ▼
  Leaderboard updated in real time
```

### Verdict Classification

| Condition | Verdict |
|---|---|
| `timeout = true` | `TIME_LIMIT_EXCEEDED` |
| `exit_code ≠ 0` | `RUNTIME_ERROR` |
| Output matches expected (all cases) | `ACCEPTED` |
| Output doesn't match | `WRONG_ANSWER` |
| Task raised an exception | `FAILED` |

### Retry Policy

The Celery task is configured with automatic retries on any unhandled exception:

- **Max retries:** 3
- **Backoff:** Exponential (`retry_backoff=True`)
- **Max backoff delay:** 60 seconds

---

## Test Results

Run:

```bash
PYTHONPATH=. pytest tests -v
```

Result:

```
23 passed
```

Generate coverage:

```bash
PYTHONPATH=. pytest tests \
  --cov=app \
  --cov-report=term-missing
```

### Coverage Summary

| Metric | Value |
|---|---|
| Total Coverage | 72% |
| API Tests | 19 |
| Worker Tests | 4 |
| **Total Automated Tests** | **23** |

### Test Breakdown

| Category | Tests |
|---|---|
| Authentication | 3 |
| Problems | 4 |
| Languages | 3 |
| Test Cases | 3 |
| Leaderboard | 2 |
| Submissions | 4 |
| Execution Worker | 4 |
| **Total** | **23** |

---

## Sandbox Validation

The Docker execution environment was manually validated.

### Network Isolation

```bash
docker run --rm \
  --network none \
  python:3.12-slim \
  python -c "import socket; socket.create_connection(('google.com',80), timeout=2)"
```

Result:

```
socket.gaierror: Temporary failure in name resolution
```

### Memory Restriction

```bash
docker run --rm \
  --memory 128m \
  python:3.12-slim \
  python -c "
x=[]
while True:
    x.append('x'*1024*1024)
"
```

Result:

```
Exit Code 137 (OOM Kill)
```

### CPU Restriction

```bash
docker run --rm \
  --cpus 0.5 \
  python:3.12-slim \
  python -c "while True: pass"
```

Result:

```
CPU throttled by Docker runtime.
```

### Verified Controls

- ✅ Network Disabled
- ✅ Memory Limited
- ✅ CPU Limited
- ✅ Timeout Enforcement
- ✅ Automatic Container Cleanup

---

## Security Design

### Authentication

```
┌────────┐         ┌───────────┐         ┌──────────┐
│ Client │──login──►│  FastAPI   │──verify──►│ Database │
│        │◄─JWT────│           │◄─user────│          │
└────────┘         └───────────┘         └──────────┘

     On each subsequent request:
     Authorization: Bearer <access_token>
           │
           ▼
     JWT decoded → user_id extracted → user loaded from DB
```

- **Password hashing:** bcrypt via `passlib` with auto-deprecation of older schemes.
- **Access tokens:** HS256-signed JWTs. Contain `sub` (user ID) and `email`. Expire after a configurable duration (default: 15 minutes).
- **Refresh tokens:** Separate HS256 JWTs with `type: "refresh"`. Stored in the `refresh_tokens` table with a `is_revoked` flag. Expire after a configurable duration (default: 7 days).
- **Token validation:** Every protected endpoint uses the `get_current_user` dependency which decodes the JWT, extracts the `sub` claim, and fetches the user from the database. Invalid or expired tokens return `401 Unauthorized`.

### Authorization (RBAC)

Three roles with hierarchical permissions:

| Role | Capabilities |
|---|---|
| **User** | Submit code, view problems, view own submissions, view leaderboard |
| **Moderator** | Everything User can do + create/update problems |
| **Admin** | Everything Moderator can do + delete problems, manage languages, manage test cases, update user roles |

Role enforcement uses the `require_roles` dependency:

```python
@router.post("/problems")
async def create_problem(
    current_user: Annotated[
        User,
        Depends(require_roles([UserRole.ADMIN, UserRole.MODERATOR]))
    ],
): ...
```

Submissions enforce **ownership checks** — users can only view their own submissions. Admins can view any submission.

### Sandbox Security

User-submitted code runs in ephemeral Docker containers with strict isolation:

| Control | Value | Purpose |
|---|---|---|
| `--network none` | Network disabled | Prevent internet access, data exfiltration |
| `--memory 128m` | 128 MB RAM cap | Prevent memory exhaustion on host |
| `--cpus 0.5` | Half a CPU core | Prevent CPU starvation of other processes |
| `--rm` | Auto-remove on exit | No container accumulation |
| `timeout` | 2 seconds (configurable) | Kill long-running or infinite-loop code |
| Volume mount | Read-only code dir | Only the source file is mounted |

### Rate Limiting

SlowAPI rate limits protect abuse-prone endpoints:

| Endpoint | Limit |
|---|---|
| `POST /submissions/execute` | 20 requests/minute |
| `POST /submissions/judge` | 5 requests/minute |

Exceeded limits return `429 Too Many Requests`.

### Observability

- **Structured logging** — Loguru with console output and rotating file logs (`logs/app.log`, 10 MB rotation, 10 day retention, gzip compression).
- **Prometheus metrics** — Exposed at `/metrics`:
  - `submission_total` — Counter of all submissions processed
  - `accepted_total` — Counter of accepted submissions
  - `execution_runtime_seconds` — Histogram of code execution times

---

## Future Enhancements

Potential future improvements:

- Additional Language Support (Java, C++, Go)
- Contest Management System
- Code Plagiarism Detection
- Submission Replay
- Distributed Worker Scaling
- Kubernetes Deployment
- Redis Caching Layer
- Organization / Team Leaderboards
- Custom Test Case Execution History

---

## Demo Walkthrough

Suggested flow to explore the platform:

1. **Login as User** — `user@test.com` / `User123!`
2. **Browse Problems** — View the problem list
3. **Open a Problem** — Read statement, constraints, and sample I/O
4. **Submit a Solution** — Write code and execute against sample cases
5. **Observe Real-Time Updates** — Watch WebSocket status transitions (`PENDING` → `RUNNING` → `ACCEPTED`)
6. **Judge Submission** — Submit for official judging against hidden test cases
7. **View Submission History** — Review past submissions and verdicts
8. **View Leaderboard** — Check rankings after accepted submissions
9. **Login as Admin** — `admin@test.com` / `Admin123!`
10. **Manage Content** — Create/edit problems, add test cases, manage languages

---

## Project Status

**Current Status:** Completed

### Implemented

- Authentication & Authorization
- Problem Management
- Test Case Management
- Submission Processing
- Docker Sandbox Execution
- WebSocket Updates
- Leaderboard System
- Prometheus Metrics
- Automated Testing
- Seed Data Script

### Statistics

| Metric | Value |
|---|---|
| Supported Languages | 2 |
| Automated Tests | 23 |
| Code Coverage | 72% |
| Docker Sandbox | Verified |
| Real-Time Updates | WebSocket |
| Seed Data | 2 users, 5 problems, 15 test cases |
