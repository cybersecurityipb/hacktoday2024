FROM ubuntu:lunar

EXPOSE 1475

RUN apt-get update && apt-get upgrade -y && apt-get update --fix-missing
RUN apt-get install -y python3 socat

RUN mkdir /osint
COPY server.py /osint/server.py

WORKDIR /osint

RUN chmod -R 755 /osint/

RUN chmod 700  /tmp /dev/shm
RUN chmod 755 /usr/bin/env /usr/bin/python3 /bin/dash /bin/bash /bin/sh /bin/cat /usr/bin/groups /usr/bin/id /bin/ls

RUN chmod +x /osint/server.py

CMD socat TCP-LISTEN:1475,reuseaddr,fork EXEC:/osint/server.py,su=nobody