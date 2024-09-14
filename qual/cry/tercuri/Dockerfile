FROM python:3.10-slim

EXPOSE 5000

RUN pip install pycryptodome && \
    apt-get update && apt-get install -y socat && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /challs
COPY server.py /challs/server.py
COPY tersangka.txt /challs/tersangka.txt
WORKDIR /challs

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:python server.py"]