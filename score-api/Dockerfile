FROM python:3.12-slim AS builder

WORKDIR /build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml .
COPY score_service/ score_service/
RUN uv pip install --system --no-cache .

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn
COPY score_service/ score_service/

ENV SCORE_SERVICE_PORT=8080
ENV SCORE_LOG_LEVEL=INFO
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; \
sys.exit(0 if urllib.request.urlopen('http://localhost:'+__import__('os').environ.get('SCORE_SERVICE_PORT','8080')+'/health', timeout=2).status==200 else 1)"

CMD ["sh", "-c", "exec uvicorn score_service.main:app --host 0.0.0.0 --port ${SCORE_SERVICE_PORT:-8080} --log-level ${SCORE_LOG_LEVEL:-info}"]
