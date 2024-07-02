FROM ubuntu:jammy

EXPOSE 8000

RUN mkdir /pwn
WORKDIR /pwn

RUN apt update
RUN apt-get install -y socat python3

COPY . .

CMD socat TCP-LISTEN:8000,reuseaddr,fork EXEC:/pwn/yesjail.py,su=nobody
