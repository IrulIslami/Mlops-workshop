FROM python:3.10-slim

WORKDIR /app

# Install system deps yang sering diperlukan (opsional, tetap ringan)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

# Salin requirements dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin source & artefak model
COPY src ./src
COPY models ./models

EXPOSE 8000
CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8000"]
