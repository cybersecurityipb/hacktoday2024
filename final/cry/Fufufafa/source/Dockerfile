FROM python:3.10-slim

EXPOSE 5000

ARG binary
ENV binary=${binary}

RUN pip install pycryptodome numpy fastecdsa && \
    apt-get update && apt-get install -y socat && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir /challs
COPY $binary /challs/$binary
COPY server.py /challs/server.py
WORKDIR /challs

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:python server.py"]