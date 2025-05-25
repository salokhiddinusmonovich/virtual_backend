FROM python:3.10.12-alpine

WORKDIR /code

COPY requirements.txt /code/

# Add system dependencies for psycopg2
RUN apk add --no-cache gcc musl-dev postgresql-dev

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/
