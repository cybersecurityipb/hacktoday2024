FROM ubuntu:jammy

EXPOSE 8000

RUN dpkg --add-architecture i386
RUN apt update && apt upgrade -y && apt update --fix-missing
RUN apt-get install -y socat
RUN apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386

RUN mkdir /pwn
COPY flag.txt /pwn/flag.txt
COPY hmmhow /pwn/hmmhow
WORKDIR /pwn

RUN chown -R 755 /pwn
RUN chmod 700 /usr/bin/* /bin/* /tmp /dev/shm
RUN chmod 755 /usr/bin/env /bin/dash /bin/bash /bin/sh /bin/cat /usr/bin/id /bin/ls 
RUN chmod +x /pwn/hmmhow

CMD socat TCP-LISTEN:8000,reuseaddr,fork EXEC:/pwn/hmmhow,su=nobody