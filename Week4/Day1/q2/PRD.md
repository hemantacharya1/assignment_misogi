# AI-Powered Product Recommendation System – PRD & Development Guidelines

## 1. Purpose
Build a **full-stack web application** that ingests a provided `mock_data.json` product catalog, allows users to register/login, browse products, and receive personalised recommendations powered by classical ML and (optionally) Gemini re-ranking.  
This document is the single source of truth; the engineering team **must not introduce features, files, or endpoints that are not explicitly listed here without prior product-owner approval**.

## 2. Scope
### 2.1 Features (MVP)
1. **User Authentication**  
   • Register, Login (email + password, bcrypt hash)  
   • JWT returned on successful login  
   • Auth middleware for protected routes
2. **Product Catalog**  
   • Import products from `backend/mock_data.json` into PostgreSQL on server start  
   • List view with search + category filter  
   • Product detail view
3. **User Interactions**  
   • Track `view`, `like`, `purchase` events via `/interactions` endpoint
4. **Recommendation Engine – Phase 1**  
   • Content-based filtering (TF-IDF on name, description, category)  
   • Return top-N products via `/recommendations` for current user
5. **Recommendation Engine – Phase 2 (Stretch)**  
   • Simple collaborative filtering (cosine similarity on user–item matrix)  
   • Gemini API re-ranking + explanation text (optional, behind feature flag)
6. **Responsive Front-end** (React + Vite + Tailwind)  
   • Routes: `/login`, `/register`, `/products`, `/product/:id`  
   • Auth context + Axios interceptor  
   • Recommendations shown on home/dashboard and product detail pages
7. **Testing**  
   • Pytest + httpx for FastAPI endpoints (auth, products, recommendations)  
   • Jest + React Testing Library for critical UI components
8. **Documentation**  
   • Update this PRD if scope changes  
   • `README.md` with setup, run, and test instructions

### 2.2 Out-of-Scope (Explicitly NOT to be built)
• Payments or real checkout flow  
• Admin dashboards  
• Multi-language support  
• Real-time websockets  
• Any UI/UX beyond what is necessary for feature list above

## 3. Tech Stack
Backend: **FastAPI, PostgreSQL 17 (SQLModel/SQLAlchemy), Uvicorn, psycopg, python-dotenv, passlib[bcrypt], PyJWT, scikit-learn, numpy**  
Front-end: **React 18, Vite, TailwindCSS ^3, React Router v6, Axios**  
LLM: **Gemini API (optional, phase 2)**  
Testing: **Pytest, httpx, Jest, @testing-library/react**

## 4. Data Model (PostgreSQL)
• `users`(id, email, hashed_password, created_at)  
• `products`(id, name, category, price, description, rating, image_url, ...from JSON)  
• `interactions`(id, user_id, product_id, type, timestamp)

## 5. API Endpoints
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /auth/register | ❌ | email, password → JWT |
| POST | /auth/login | ❌ | email, password → JWT |
| GET | /products | ❌ | List products, optional `search`, `category` |
| GET | /products/{id} | ❌ | Product detail |
| POST | /interactions | ✅ | Body: product_id, type(view/like/purchase) |
| GET | /recommendations | ✅ | Return top-N recommended products |

*No other endpoints are to be created without product-owner approval.*

## 6. Recommendation Logic – Phase 1 (Baseline)
1. Compute TF-IDF matrix on `name + description + category` once at startup.  
2. For anonymous users → return globally popular products (top ratings).  
3. For logged-in users → build user profile vector from liked/purchased products; compute cosine similarity against catalog; filter out already purchased items; return top-N.

## 7. Milestones & Timeline
| Milestone | Description | Target |
|-----------|-------------|--------|
| M0 | Repo skeleton, Prettier/ESLint, CI | Day 0 |
| M1 | Backend: JSON import + /products endpoints | Day 1 |
| M2 | Auth (register/login) | Day 2 |
| M3 | Front-end auth flow + catalog UI | Day 3 |
| M4 | Interaction tracking endpoints + client hooks | Day 4 |
| M5 | Content-based recommender + UI | Day 5 |
| M6 | Tests for auth & recommender | Day 6 |
| M7 | (Stretch) Collaborative filtering & Gemini | Day 7 |

## 8. Acceptance Criteria & Definition of Done
1. All endpoints pass tests in CI.  
2. User can register, login, browse products, and receive non-empty personalised recommendations.  
3. Lighthouse mobile performance ≥ 80.  
4. README provides clear setup/run/test steps.  
5. No lint errors (`ruff` + ESLint).  
6. PR merged only if features comply with this PRD.  

## 9. Anti-Hallucination Guidelines for AI Assistants
1. **Stick to this PRD.** If a requested feature/API/file is not covered here, flag it and request clarification.
2. **No extra dependencies** beyond tech stack above unless justified and approved.
3. **Cite code** with file-path and line numbers when referencing existing code.
4. **Use parallel tool calls** when reading/searching files; avoid unnecessary sequential steps.
5. **Do NOT generate boilerplate code in discussion messages.** Use code-edit operations when implementation is required.
6. **Ask for clarification** instead of guessing when requirements are ambiguous.

## 3.1 Environment Variables (.env)
```
DATABASE_URL=postgresql+psycopg://<user>:<password>@localhost:5432/<dbname>
JWT_SECRET=<super-secret-key>
JWT_EXPIRE_MIN=60
GEMINI_API_KEY=<optional>
```
_Add additional variables here only with product-owner approval._

## 3.2 Git Hygiene
• Add `venv/` and other virtual‐env folders to `.gitignore` so they never reach the repo.

---
_Last updated: {{DATE}} by Product Owner_ 