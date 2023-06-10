FROM python:3.10.11-slim-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
WORKDIR /evalquiz-material-server
CMD ["gunicorn", "evalquiz-material-server:app", "-b", "0.0.0.0:80"]