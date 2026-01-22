# Gunakan image Python yang stabil dan ringan
FROM python:3.11-slim

# Atur environment variable untuk menghindari penulisan file .pyc dan buffering log
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Tentukan direktori kerja di dalam container
WORKDIR /app

# Install dependencies sistem yang diperlukan untuk library Python tertentu
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Buat user baru dengan ID 1000 (standar keamanan Hugging Face)
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Salin file requirements.txt terlebih dahulu agar cache layer Docker efisien
COPY --chown=user requirements.txt .

# Install semua library Python yang dibutuhkan
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Salin seluruh file proyek (termasuk main.py, olist.db, dan folder agents) ke dalam container
COPY --chown=user . .

# Hugging Face menggunakan port 7860 secara default
ENV PORT=7860
EXPOSE 7860

# Perintah untuk menjalankan Backend FastAPI Anda
# Menggunakan uvicorn untuk menjalankan 'app' yang ada di dalam 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]