FROM debian:bookworm-20240812

RUN apt-get update
RUN apt-get install --no-install-recommends sudo python3 python3-pip iputils-ping vim procps -y
RUN apt-get autoremove --purge && apt-get clean

RUN mkdir /ctf
RUN addgroup --system --gid 1000 michie
RUN adduser --system --uid 1000 --ingroup michie --home /ctf michie --shell /bin/bash
RUN echo "michie ALL=(ALL) NOPASSWD: /usr/bin/view" >> /etc/sudoers
RUN chown michie:michie /ctf
WORKDIR /ctf

COPY --chown=michie:michie src src
COPY --chown=michie:michie requirements.txt .
COPY --chown=michie:michie run.sh .
COPY --chown=root:root flag.txt src/flag.txt
COPY --chown=root:root get_flag.run src/get_flag.run

RUN pip install -U pip --break-system-packages --no-cache-dir
RUN pip install -r requirements.txt --break-system-packages --no-cache-dir

RUN rm -rf /ctf/src/databases
RUN mkdir -p /ctf/src/databases
RUN chown michie:michie /ctf/src/databases

RUN rm -rf /ctf/src/__pycache__
RUN mkdir -p /ctf/src/__pycache__
RUN chown michie:michie /ctf/src/__pycache__

RUN chmod 400 /ctf/src/flag.txt
RUN chmod 500 /ctf/src/get_flag.run
RUN chmod 555 /ctf/run.sh

USER michie
CMD /ctf/run.sh
