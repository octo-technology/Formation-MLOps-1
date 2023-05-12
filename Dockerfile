# set base image
FROM python:3.11

COPY ./src /src
COPY ./setup.py /setup.py
COPY ./requirements.txt /requirements.txt

COPY ./models /models

COPY ./api /api

RUN pip install --no-cache-dir .

EXPOSE 80:80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
