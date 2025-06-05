FROM python:3.10-slim

WORKDIR /app

# Primeiro copiar apenas requirements.txt para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências durante o build
RUN pip install --no-cache-dir -r requirements.txt

# Agora copiar o resto dos arquivos
COPY . .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD python3 /app/healthcheck.py

# Comando de inicialização direto
CMD ["python3", "bot_telegram.py"]
