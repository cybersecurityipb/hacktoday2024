FROM python:3.10-slim

EXPOSE 5000

RUN apt-get update && \
    apt-get install -y gcc libgmp-dev build-essential socat && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install pycryptodome numpy fastecdsa

RUN mkdir /challs
COPY server.py /challs/server.py
COPY utils.py /challs/utils.py
WORKDIR /challs

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:python server.py"]