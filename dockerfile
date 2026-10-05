FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY generator/ ./generator/

EXPOSE 8000

CMD ["uvicorn", "generator.main:app", "--host", "0.0.0.0", "--port", "8000"]