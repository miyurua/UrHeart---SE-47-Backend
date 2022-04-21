# Dockerfile specifies hoe to build a Docker image

FROM python:3.9.7

ADD . /code
WORKDIR /code

RUN pip install -r requirements.txt

ENTRYPOINT [ "python","app.py" ]