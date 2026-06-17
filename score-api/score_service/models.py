from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Dimensions(BaseModel):
    governance: float = Field(ge=0.0, le=100.0)
    innovation: float = Field(ge=0.0, le=100.0)
    operations: float = Field(ge=0.0, le=100.0)
    finance: float = Field(ge=0.0, le=100.0)
    sustainability: float = Field(ge=0.0, le=100.0)

    model_config = {
        "json_schema_extra": {
            "example": {
                "governance": 80.0,
                "innovation": 70.0,
                "operations": 65.0,
                "finance": 75.0,
                "sustainability": 72.0,
            }
        }
    }


class ScoreRequest(BaseModel):
    company_id: UUID
    dimensions: Dimensions

    model_config = {
        "json_schema_extra": {
            "example": {
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "dimensions": {
                    "governance": 80.0,
                    "innovation": 70.0,
                    "operations": 65.0,
                    "finance": 75.0,
                    "sustainability": 72.0,
                },
            }
        }
    }


class ScoreResponse(BaseModel):
    company_id: str
    composite_score: float
    grade: str
    dimension_scores: Dimensions
    computed_at: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "company_id": "123e4567-e89b-12d3-a456-426614174000",
                "composite_score": 72.8,
                "grade": "B",
                "dimension_scores": {
                    "governance": 80.0,
                    "innovation": 70.0,
                    "operations": 65.0,
                    "finance": 75.0,
                    "sustainability": 72.0,
                },
                "computed_at": "2026-06-17T10:00:00Z",
            }
        }
    }
