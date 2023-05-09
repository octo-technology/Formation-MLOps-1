# set base image
FROM python:3.11

WORKDIR /code

COPY ./src /code/src
COPY ./setup.py /code/setup.py
COPY ./requirements.txt /code/requirements.txt

COPY ./models /code/models

COPY ./api /code/api

RUN pip install --no-cache-dir .

EXPOSE 80:80

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "80"]
