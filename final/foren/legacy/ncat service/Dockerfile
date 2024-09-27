FROM python:3.10-slim-buster

RUN apt-get update
RUN apt-get install -y nano socat gcc libgmp3-dev
RUN pip install -U pip
RUN pip install fastecdsa

WORKDIR /opt
COPY src/run.py .

RUN chmod +x run.py
CMD socat TCP-LISTEN:8081,fork,reuseaddr EXEC:'python3 -u run.py'