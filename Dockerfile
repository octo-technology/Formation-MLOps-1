FROM python:3.15-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.5 /uv /uvx /bin/

WORKDIR /app
ENV UV_PYTHON_DOWNLOADS=never \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --locked --no-dev --no-install-project

COPY src ./src
RUN uv sync --locked --no-dev --no-editable

COPY models ./models
COPY api ./api

EXPOSE 80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
