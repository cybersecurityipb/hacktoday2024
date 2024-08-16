FROM php:8.1-cli

# Set the working directory
WORKDIR /var/www/html

# Copy all files to the working directory
COPY . /var/www/html

RUN echo "output_buffering = 8192" > /usr/local/etc/php/php.ini

# Switch to the 'nobody' user for better security
USER nobody

# Expose port 20000 for external access
EXPOSE 20000


# Start the PHP built-in server
CMD [ "php", "-S", "0.0.0.0:20000", "-t", "/var/www/html" ]
