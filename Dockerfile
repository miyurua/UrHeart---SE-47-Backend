# syntax=docker/dockerfile:1

FROM python:3.9.7-slim as base

# Install python dependencies in /.venv

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

# Install pipenv

RUN pip install pipenv

RUN pipenv shell

WORKDIR /UrHeart--SE-47-Backend

RUN pipenv sync

EXPOSE 5000

CMD ["python", "app.py"]