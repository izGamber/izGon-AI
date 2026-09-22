# Dockerfile - Production setup za izGon-AI

FROM python:3.11-slim

WORKDIR /app

# Instaliraj sistemske zavisnosti
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Kopiraj requirements
COPY requirements.txt .

# Instaliraj Python zavisnosti
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj aplikaciju
COPY . .

# Kreiraj data direktorijum
RUN mkdir -p data

# Expose port
EXPOSE 8000

# Environment
ENV PYTHONUNBUFFERED=1
ENV DEBUG=False

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Start aplikaciju
CMD ["uvicorn", "app.dashboard:asgi_app", "--host", "0.0.0.0", "--port", "8000"]
