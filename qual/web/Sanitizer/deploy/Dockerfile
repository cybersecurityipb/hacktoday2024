FROM php:8.1-cli
WORKDIR /var/www/html
COPY . /var/www/html
USER nobody
EXPOSE 20000

CMD [ "php", "-S", "0.0.0.0:20000", "-t", "/var/www/html" ]
