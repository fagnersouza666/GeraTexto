FROM python:3.10-slim

WORKDIR /app

# Copiar arquivos
COPY requirements.txt .
COPY . .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD python3 /app/healthcheck.py

# Comando de inicialização direto
CMD ["python3", "bot_telegram.py"]
