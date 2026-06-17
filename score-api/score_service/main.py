from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI

from .models import ScoreRequest, ScoreResponse
from .scoring import assign_grade, compute_composite

_DESCRIPTION = """
Evaluates companies across five dimensions and returns a composite health score.

## Scoring

Each dimension is rated **0–100**. The composite score is a weighted average:

| Dimension      | Weight |
|----------------|--------|
| Governance     | 25%    |
| Innovation     | 20%    |
| Operations     | 20%    |
| Finance        | 20%    |
| Sustainability | 15%    |

## Grades

| Score  | Grade |
|--------|-------|
| ≥ 85   | A     |
| ≥ 70   | B     |
| ≥ 55   | C     |
| < 55   | D     |
"""


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Company Health Score API",
    description=_DESCRIPTION,
    version="0.1.0",
    lifespan=lifespan,
)


@app.get(
    "/health",
    summary="Liveness probe",
    description="Returns `{\"status\": \"ok\"}` when the service is running.",
    tags=["health"],
)
def health():
    return {"status": "ok"}


@app.post(
    "/score",
    response_model=ScoreResponse,
    summary="Compute company health score",
    description=(
        "Accepts dimension scores for a company and returns the weighted composite "
        "score together with a letter grade and the individual dimension values."
    ),
    responses={
        422: {
            "description": "Dimension value outside [0, 100] or required field missing."
        },
    },
    tags=["scoring"],
)
def score(body: ScoreRequest):
    composite_score = compute_composite(body.dimensions.model_dump())
    return ScoreResponse(
        company_id=str(body.company_id),
        composite_score=composite_score,
        grade=assign_grade(composite_score),
        dimension_scores=body.dimensions,
        computed_at=datetime.now(timezone.utc),
    )
