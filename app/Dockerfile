FROM python:3.8 as base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y sudo && apt-get install build-essential python3-dev -y
RUN pip install --upgrade pip && pip install -U pip setuptools wheel && pip install uwsgi

RUN mkdir -p /application/logs && mkdir -p /application/uwsgi

WORKDIR /application/acce_shop/app
RUN mkdir static && mkdir media

COPY Pipfile .
COPY Pipfile.lock .
RUN pip install pipenv && pipenv install --ignore-pipfile --system --deploy --dev
COPY . .

RUN groupadd --gid 5000 admin \
    && useradd --home-dir /home/admin --create-home --uid 5000 --gid 5000 -G sudo,www-data --shell /bin/sh admin

RUN chown -R admin:admin /application \
    && chown admin:www-data /application/uwsgi \
    && chmod -R 770 /application/uwsgi \
    && chmod +x entrypoint.sh

USER admin
