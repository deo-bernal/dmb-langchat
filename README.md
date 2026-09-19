# DMB LangChat

Python LangChain chat with **durable memory in Convex** (Free tier). Sibling product — not part of dmbportfolio.

## Stack

| Layer | Host | Role |
| --- | --- | --- |
| Web | Vercel | Chat UI, Convex realtime |
| Convex | Convex Cloud Free | `threads` + `messages` |
| API | Render Free | FastAPI + LangChain (Gemini) via `convex-py` |

## Local run

### 1. Convex

```bash
cd C:\github\Deo\dmb-langchat
npm install
npx convex dev
```

Copy the deployment URL into `api/.env` and `web/.env.local`.

### 2. Python API

```bash
cd api
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# set CONVEX_URL, GOOGLE_API_KEY
uvicorn main:app --reload --port 8080
```

### 3. Web

```bash
cd web
npm install
copy .env.example .env.local
# set VITE_CONVEX_URL, VITE_API_URL=http://localhost:8080
npm run dev
```

## Docs

PDFs in `Documentations/` — regenerate with:

```bash
cd Documentations
python _build_sso_pdf.py
python _build_architecture_pdf.py
python _build_user_guide_pdf.py
```

## Deploy

- `npx convex deploy`
- Render: Docker or native Python from `api/`
- `cd web && npx vercel --prod`
