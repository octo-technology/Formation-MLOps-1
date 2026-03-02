# set base image
FROM python:3.14

COPY ./src /src
COPY pyproject.toml /pyproject.toml
COPY uv.lock /uv.lock
COPY ./models /models

COPY ./api /api

RUN uv sync

EXPOSE 80:80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
