# Memaksa server menggunakan Python 3.12
FROM python:3.12-slim

# Menyiapkan folder kerja
WORKDIR /app

# Menginstal semua dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin seluruh kode Django Anda ke server
COPY . .

# Pindah ke folder yang berisi manage.py
WORKDIR /app/config

# Mengumpulkan static file dan memastikan database terhubung
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Ubah baris CMD paling bawah menjadi seperti ini:
EXPOSE 8080
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8080"]