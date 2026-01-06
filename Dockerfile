FROM python:3.11-slim
WORKDIR /app

# 1. Instalasi dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Salin file proyek (Selektif seperti permintaan Anda)
COPY agents/ ./agents/
COPY olist.db .
COPY streamlit_app.py .

# 3. Konfigurasi Environment
ENV PYTHONPATH=/app

EXPOSE 8501

# 4. Perintah menjalankan aplikasi (Gunakan python -m)
CMD ["python", "-m", "streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]