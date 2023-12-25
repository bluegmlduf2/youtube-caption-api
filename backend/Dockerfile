FROM python:3.9-alpine3.18

WORKDIR /backend
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt