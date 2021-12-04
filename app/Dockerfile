FROM python:3.8 as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /application
RUN mkdir -p logs
WORKDIR acce_shop

COPY Pipfile .
COPY Pipfile.lock .
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --ignore-pipfile --system --deploy --dev
COPY . .