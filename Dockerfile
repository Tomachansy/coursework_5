FROM python:3.10-slim-bullseye

ENV FLASK_APP game.app:app

WORKDIR /code

COPY requirements.txt .

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

COPY . .
