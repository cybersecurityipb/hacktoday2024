FROM python:3.11-slim

ARG GECKODRIVER_VERSION
ARG SELENIUM_VERSION

RUN apt-get update && \
    apt-get install --no-install-recommends -y wget postgresql-15 postgresql-client-15 postgresql-contrib-15 libpq-dev firefox-esr

RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v${GECKODRIVER_VERSION}/geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz && \
    tar -xvzf geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz && \
    mv geckodriver /usr/local/bin/ && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v${GECKODRIVER_VERSION}-linux64.tar.gz

RUN su postgres -c '/usr/lib/postgresql/15/bin/pg_ctl -D /var/lib/postgresql/data initdb'

RUN pip install psycopg2-binary flask selenium==${SELENIUM_VERSION}

WORKDIR /app
COPY ./src /app/
COPY ./flag.txt /flag
RUN mv /flag /flag_$(head /dev/urandom | tr -dc 'A-Za-z0-9' | head -c 32).txt

RUN chmod +x /app/start.sh

EXPOSE 5000

CMD ["/app/start.sh"]