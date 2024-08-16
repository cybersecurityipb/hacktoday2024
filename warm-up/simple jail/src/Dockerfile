FROM python:3.11

EXPOSE 9001

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y socat

COPY . .

CMD socat TCP-LISTEN:9001,reuseaddr,fork EXEC:/usr/src/app/simple_jail.py,su=nobody
