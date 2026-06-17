WEIGHTS: dict[str, float] = {
    "governance": 0.25,
    "innovation": 0.20,
    "operations": 0.20,
    "finance": 0.20,
    "sustainability": 0.15,
}


def compute_composite(dimensions: dict[str, float]) -> float:
    return round(sum(dimensions[k] * w for k, w in WEIGHTS.items()), 2)


def assign_grade(score: float) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    return "D"
