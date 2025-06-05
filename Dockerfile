FROM python:3.10-slim

# Variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Diretório de trabalho
WORKDIR /app

# Copiar código
COPY . .

# Comando de execução
CMD ["./start.sh"]
