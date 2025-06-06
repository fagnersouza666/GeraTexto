FROM python:3.10-slim

WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
COPY . .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=15s --start-period=120s --retries=3 \
    CMD python3 /app/healthcheck.py

# Usar start.sh que instala dependências
CMD ["bash", "start.sh"]
