FROM php:8.1-cli

WORKDIR /var/www/html
COPY web/ /var/www/html
COPY flag.txt /.flag
RUN echo "output_buffering = 8192" > /usr/local/etc/php/php.ini
USER nobody
EXPOSE 80

CMD [ "php", "-S", "0.0.0.0:80", "-t", "/var/www/html/public" ]