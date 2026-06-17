import pytest

from score_service.scoring import assign_grade, compute_composite

VALID_DIMS = {
    "governance": 80.0,
    "innovation": 70.0,
    "operations": 65.0,
    "finance": 75.0,
    "sustainability": 72.0,
}

VALID_PAYLOAD = {
    "company_id": "123e4567-e89b-12d3-a456-426614174000",
    "dimensions": {
        "governance": 80.0,
        "innovation": 70.0,
        "operations": 65.0,
        "finance": 75.0,
        "sustainability": 72.0,
    },
}


@pytest.mark.asyncio
async def test_score_returns_200(client):
    response = await client.post("/score", json=VALID_PAYLOAD)
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_score_composite_and_grade(client):
    response = await client.post("/score", json=VALID_PAYLOAD)
    data = response.json()
    
    assert data["composite_score"] == 72.8
    assert data["grade"] == "B"
    assert data["company_id"] == VALID_PAYLOAD["company_id"]


@pytest.mark.asyncio
async def test_score_dimension_out_of_range(client):
    bad_dims = {**VALID_PAYLOAD["dimensions"], "governance": 101.0}
    payload = {**VALID_PAYLOAD, "dimensions": bad_dims}
    response = await client.post("/score", json=payload)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_score_missing_dimension(client):
    payload = {
        "company_id": VALID_PAYLOAD["company_id"],
        "dimensions": {
            k: v for k, v in VALID_PAYLOAD["dimensions"].items() if k != "finance"
        },
    }
    response = await client.post("/score", json=payload)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_score_response_shape(client):
    response = await client.post("/score", json=VALID_PAYLOAD)
    data = response.json()
    
    assert set(data["dimension_scores"].keys()) == {
        "governance", "innovation", "operations", "finance", "sustainability"
    }
    assert "computed_at" in data


@pytest.mark.asyncio
async def test_score_grade_a(client):
    dims = {k: 90.0 for k in VALID_PAYLOAD["dimensions"]}
    response = await client.post("/score", json={**VALID_PAYLOAD, "dimensions": dims})
    
    assert response.json()["grade"] == "A"


@pytest.mark.asyncio
async def test_score_grade_c(client):
    dims = {k: 60.0 for k in VALID_PAYLOAD["dimensions"]}
    response = await client.post("/score", json={**VALID_PAYLOAD, "dimensions": dims})
    
    assert response.json()["grade"] == "C"


@pytest.mark.asyncio
async def test_score_grade_d(client):
    dims = {k: 40.0 for k in VALID_PAYLOAD["dimensions"]}
    response = await client.post("/score", json={**VALID_PAYLOAD, "dimensions": dims})
    
    assert response.json()["grade"] == "D"


@pytest.mark.asyncio
async def test_score_boundary_values_valid(client):
    dims = {k: 0.0 for k in VALID_PAYLOAD["dimensions"]}
    response = await client.post("/score", json={**VALID_PAYLOAD, "dimensions": dims})
    
    assert response.status_code == 200

    dims = {k: 100.0 for k in VALID_PAYLOAD["dimensions"]}
    response = await client.post("/score", json={**VALID_PAYLOAD, "dimensions": dims})
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_score_negative_value(client):
    bad_dims = {**VALID_PAYLOAD["dimensions"], "operations": -1.0}
    payload = {**VALID_PAYLOAD, "dimensions": bad_dims}
    response = await client.post("/score", json=payload)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_score_invalid_company_id(client):
    payload = {**VALID_PAYLOAD, "company_id": "not-a-uuid"}
    response = await client.post("/score", json=payload)
    
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_score_empty_body(client):
    response = await client.post("/score", json={})

    assert response.status_code == 422


def test_compute_composite_known_values():
    assert compute_composite(VALID_DIMS) == 72.8


def test_compute_composite_all_zeros():
    assert compute_composite({k: 0.0 for k in VALID_DIMS}) == 0.0


def test_compute_composite_all_hundreds():
    assert compute_composite({k: 100.0 for k in VALID_DIMS}) == 100.0


def test_compute_composite_uniform_value():
    assert compute_composite({k: 60.0 for k in VALID_DIMS}) == 60.0


@pytest.mark.parametrize("score,expected_grade", [
    (100.0, "A"),
    (85.0, "A"),
    (84.9, "B"),
    (70.0, "B"),
    (69.9, "C"),
    (55.0, "C"),
    (54.9, "D"),
    (0.0, "D"),
])
def test_assign_grade_boundaries(score, expected_grade):
    assert assign_grade(score) == expected_grade
