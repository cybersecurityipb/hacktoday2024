FROM httpd:2.4.50

# Salin file HTML kustom ke dalam container
COPY custom_404.html /usr/local/apache2/htdocs/custom_404.html

# Salin konfigurasi kustom untuk Apache
COPY httpd.conf /usr/local/apache2/conf/httpd.conf

# Buat direktori untuk file error kustom
RUN mkdir -p /usr/local/apache2/error

# Salin file HTML kustom sebagai halaman 404
COPY custom_404.html /usr/local/apache2/error/custom_404.html

# Salin file index.html kustom ke dalam container
COPY index.html /usr/local/apache2/htdocs/index.html
COPY flag.txt /flag.txt