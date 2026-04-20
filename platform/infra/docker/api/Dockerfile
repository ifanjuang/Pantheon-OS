FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY platform/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI application (runs as the working directory)
COPY platform/api/ .

# Hermes Runtime framework (auto-discovery)
COPY core/ /core/
COPY modules/ /modules/

# Config files
COPY config/ /config/

# Domain overlays
COPY domains/ /domains/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
