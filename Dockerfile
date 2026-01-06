FROM python:3.11-slim
WORKDIR /app

# Install dependencies sistem
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file ke dalam docker
COPY . .

# Jalankan backend API secara default (Port 8080 untuk Railway)
ENV PORT=8080
EXPOSE 8080

# Menjalankan API menggunakan Uvicorn
CMD ["python", "main.py"]