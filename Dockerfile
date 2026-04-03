# set base image
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

COPY ./src /src
COPY pyproject.toml /pyproject.toml
COPY uv.lock /uv.lock
COPY ./models /models

COPY ./api /api

RUN uv sync

EXPOSE 80:80

CMD ["uv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
