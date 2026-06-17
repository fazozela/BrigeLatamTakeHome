# Dashboard UI

Nuxt 3 frontend that displays the Company Health Score widget. Proxies all requests to the score API through a server-side route so the upstream URL is never exposed to the browser.

## Requirements

- Node.js 18+
- Score API running (see root README)

## Setup

```bash
npm install
```

## Running locally

```bash
npm run dev
```

App available at `http://localhost:3000`.

## Environment variables

| Variable | Default | Description |
|---|---|---|
| `NUXT_SCORE_SERVICE_URL` | `http://localhost:8000` | URL of the score API |

## Structure

```
components/CompanyScoreWidget.vue   # Score widget (loading, error, data states)
server/api/score.post.ts            # Server-side proxy to the score API
pages/index.vue                     # Entry page
nuxt.config.ts                      # Runtime config (scoreServiceUrl, private)
```
