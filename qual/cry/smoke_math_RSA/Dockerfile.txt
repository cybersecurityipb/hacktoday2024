FROM ubuntu:focal

EXPOSE 5000

ARG binary
ENV binary=${binary}

# update
RUN apt update && apt upgrade -y && apt update --fix-missing
RUN apt-get update --fix-missing
RUN apt-get install python3 python3-pip socat -y
RUN apt-get install curl -y
RUN pip3 install pycryptodome


# copy file
RUN mkdir /challs
COPY $binary /challs/$binary
COPY server.py /challs/server.py
COPY flag.txt /challs/flag.txt
WORKDIR /challs

# securing flag
RUN chown -R 755 /challs/
RUN chmod +x /challs/$binary
# Securing environment
RUN chmod 700 /usr/bin/* /bin/* /tmp /dev/shm
RUN chmod 755 /usr/bin/env /usr/bin/python3 /bin/dash /bin/bash /bin/sh /bin/cat /usr/bin/curl /usr/bin/groups /usr/bin/id /bin/ls


# Run Program
CMD socat TCP-LISTEN:5000,reuseaddr,fork EXEC:/challs/$binary,su=nobody