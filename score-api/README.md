# Score Service

FastAPI service that computes a composite health score for a company based on five weighted dimensions.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- Docker (optional)

## Setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Running locally

```bash
uvicorn score_service.main:app --reload --port 8000
```

API docs available at `http://localhost:8000/docs`.

## Running tests

```bash
pytest tests/ -v
```

## Linting

```bash
ruff check score_service/ tests/
```

## Docker

```bash
docker build -t score-service .
docker run -p 8000:8080 score-service
```

The container runs uvicorn on port 8080 internally. The `-p 8000:8080` flag maps it to port 8000 on the host, which is what the dashboard expects.

## Endpoints

| Method | Path     | Description                        |
|--------|----------|------------------------------------|
| GET    | /health  | Liveness probe                     |
| POST   | /score   | Compute composite score and grade  |

### POST /score

**Request**

```json
{
  "company_id": "123e4567-e89b-12d3-a456-426614174000",
  "dimensions": {
    "governance": 80.0,
    "innovation": 70.0,
    "operations": 65.0,
    "finance": 75.0,
    "sustainability": 72.0
  }
}
```

**Response**

```json
{
  "company_id": "123e4567-e89b-12d3-a456-426614174000",
  "composite_score": 72.8,
  "grade": "B",
  "dimension_scores": {
    "governance": 80.0,
    "innovation": 70.0,
    "operations": 65.0,
    "finance": 75.0,
    "sustainability": 72.0
  },
  "computed_at": "2026-06-17T10:00:00Z"
}
```

Dimension values must be between 0 and 100. Missing or out-of-range values return HTTP 422.

## Environment variables

| Variable             | Default | Description        |
|----------------------|---------|--------------------|
| SCORE_SERVICE_PORT   | 8080    | Port to listen on  |
| SCORE_LOG_LEVEL      | INFO    | Uvicorn log level  |
