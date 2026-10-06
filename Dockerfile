FROM python:3.11-slim

WORKDIR /docs

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Puerto por defecto de MkDocs
EXPOSE 8000

# Servir con recarga automática en vivo
CMD ["mkdocs", "serve", "--dev-addr=0.0.0.0:8000"]
