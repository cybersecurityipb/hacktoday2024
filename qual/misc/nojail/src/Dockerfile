FROM python:3.11

EXPOSE 8000

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y socat

COPY . .

CMD socat TCP-LISTEN:8000,reuseaddr,fork EXEC:/usr/src/app/nojail.py,su=nobody
