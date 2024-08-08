FROM ubuntu:23.10 as ubuntu

FROM pwn.red/jail

COPY --from=ubuntu / /srv

COPY flag.txt /srv/app/flag.txt
COPY chall /srv/app/run
COPY libc.so.6 /srv/app/libc.so.6
COPY ld-linux-x86-64.so.2 /srv/app/ld-linux-x86-64.so.2
