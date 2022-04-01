# syntax=docker/dockerfile:1

FROM python:3.9.7

RUN pip install pipenv

ENV PROJECT_DIR /UrHeart--SE-47-Backend

WORKDIR ${PROJECT_DIR}

COPY Pipfile Pipfile.lock ${PROJECT_DIR}/

RUN pipenv install --system --deploy

CMD ["python","app.py"]