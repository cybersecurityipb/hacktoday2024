FROM php:8.1-cli

WORKDIR /var/www/html
COPY . /var/www/html
RUN echo "output_buffering = 8192" > /usr/local/etc/php/php.ini
USER nobody
EXPOSE 80

CMD [ "php", "-S", "0.0.0.0:80", "-t", "/var/www/html" ]
