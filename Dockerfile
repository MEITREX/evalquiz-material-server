FROM python:3.10.11-slim-buster

WORKDIR /evalquiz-material-server
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
