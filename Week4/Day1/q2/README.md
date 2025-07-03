# AI-Powered Product Recommendation App (Phase M3)

This project is the **Week 4 / Day 1 – Q2** deliverable for the assignment. It implements the first three milestones defined in `PRD.md`:

* M1 – Backend catalogue API (PostgreSQL, FastAPI)
* M2 – User authentication (JWT)
* M3 – Front-end auth flow & product catalogue UI (React + Vite + Tailwind)

> Later milestones (interaction tracking, recommender, Gemini integration) will be added incrementally.

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Backend | FastAPI, SQLModel/SQLAlchemy, PostgreSQL 17, psycopg v3, PassLib bcrypt, python-jose |
| Front-end | React 18, Vite 7, Tailwind CSS 3, React-Router 6, Axios |
| Testing | Pytest + httpx (backend), Jest + RTL (to be added) |

---

## Directory Structure

```
q2/
├─ backend/
│  ├─ main.py               # FastAPI application
│  ├─ database.py           # engine & session
│  ├─ models.py             # SQLModel tables
│  ├─ routers/              # products.py, auth.py
│  ├─ security.py           # JWT + password utils
│  ├─ tests/                # pytest suite
│  ├─ requirements.txt      # Python deps
│  ├─ env.template          # copy → .env with real creds
│  └─ mock_data.json        # initial product catalogue
├─ frontend/
│  ├─ src/                  # React code
│  ├─ package.json          # npm deps & scripts
│  ├─ tailwind.config.js
│  └─ vite.config.js
├─ PRD.md                   # Product Requirements Doc
└─ README.md                # (this file)
```

---

## Environment Variables

Create `backend/.env` (NOT committed) based on `backend/env.template`:

```
DATABASE_URL=postgresql+psycopg://<user>:<password>@localhost:5432/recommender
JWT_SECRET=<super-secret-key>
JWT_EXPIRE_MIN=60
SQL_ECHO=false
GEMINI_API_KEY=
```

Ensure PostgreSQL 17 is running and the `recommender` database exists (or change the DB name).

---

## Local Setup

### 1. Backend

```bash
# From project root
cd Week4/Day1/q2
python -m venv venv               # optional but recommended
# Windows: venv\Scripts\activate   mac/Linux: source venv/bin/activate
pip install -r backend/requirements.txt
# copy env.template → .env and edit values
uvicorn backend.main:app --reload  # http://localhost:8000
```

*On first start – tables are auto-created and `mock_data.json` is seeded into the `products` table.*

### 2. Front-end

```bash
cd frontend
npm install          # or pnpm install / yarn
npm run dev          # http://localhost:5173
```

Login/Register flows hit the backend; on success JWT is stored in `localStorage` and sent via Axios interceptor.

---

## Running Tests

```bash
# backend tests
cd Week4/Day1/q2/backend
pytest               # requires backend deps & env
```

(Front-end tests to come in later milestones.)

---

## API Reference (implemented)

| Method | Path | Description |
|--------|------|-------------|
| POST   | /auth/register | Register user, returns JWT |
| POST   | /auth/login    | OAuth2 login, returns JWT |
| GET    | /products      | List products (`search`, `category`, `page`, `page_size`) |
| GET    | /products/{id} | Product detail |

Upcoming endpoints: `/interactions`, `/recommendations` (see PRD).

---

## Roadmap

1. **M4 – User interaction tracking** (views/likes/purchases)
2. **M5 – Content-based recommender** (TF-IDF)
3. **M6 – Tests for recommender & CI workflow**
4. **M7 – Collaborative filtering + Gemini re-rank (stretch)**

---

### Author
Hemant Charya – Week 4 assignment (Masai School). 