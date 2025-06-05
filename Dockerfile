FROM python:3.10-slim

WORKDIR /app

# Copiar arquivos de dependências offline
COPY docker-deps/ /app/docker-deps/
COPY docker-requirements.txt requirements.txt

# Copiar código da aplicação
COPY . .

# Healthcheck
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=3 \
    CMD python3 /app/healthcheck.py

# Comando de inicialização
CMD ["bash", "start.sh"]
