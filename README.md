# BridgeLatam Takehome

Two services: a FastAPI scoring API and a Nuxt 3 frontend. Run both to use the app.

## Quickstart

### 1. Score API

**With Docker:**

```bash
cd score-api
docker build -t score-api .
docker run -d -p 8000:8080 score-api
```

Note: the container runs on port 8080 internally, so the mapping is `-p 8000:8080` (not `8000:8000`).

**Without Docker:**

```bash
cd score-api
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
uvicorn score_service.main:app --reload --port 8000
```

API running at `http://localhost:8000` — docs at `http://localhost:8000/docs`.

### 2. Dashboard UI

```bash
cd dashboard-ui
npm install
npm run dev
```

App running at `http://localhost:3000`.

## Services

| Service | Port | Description |
|---|---|---|
| score-api | 8000 | FastAPI — computes composite health score |
| dashboard-ui | 3000 | Nuxt 3 — displays the score widget |

## Architecture

```
Browser → POST /api/score → Nuxt server → POST http://localhost:8000/score → FastAPI
```

The browser never calls the score API directly. The Nuxt server acts as a proxy, keeping the upstream URL private.
