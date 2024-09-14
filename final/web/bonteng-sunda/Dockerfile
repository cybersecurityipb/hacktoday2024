# Gunakan image resmi Python sebagai base image
FROM python:3.11

# Setel direktori kerja di dalam container
WORKDIR /app

# Salin seluruh isi direktori saat ini ke dalam container di /app
COPY . /app

# Instal semua paket yang diperlukan sesuai dengan requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Buka port yang akan digunakan oleh aplikasi
EXPOSE 5500

# Definisikan variabel lingkungan untuk memastikan output Python tidak di-buffer
ENV PYTHONUNBUFFERED=1

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
