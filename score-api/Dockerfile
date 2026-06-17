FROM python:3.12-slim AS builder

WORKDIR /build
COPY pyproject.toml .
COPY score_service/ score_service/
RUN pip install --no-cache-dir .

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY score_service/ score_service/

ENV SCORE_SERVICE_PORT=8080
EXPOSE 8080

CMD ["uvicorn", "score_service.main:app", "--host", "0.0.0.0", "--port", "8080"]
