FROM python:3.10-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Definir diretório de trabalho
WORKDIR /app

# Copiar todo o código
COPY . .

# Script que tenta instalar dependências ou usa as disponíveis
CMD ["sh", "-c", "pip install --no-cache-dir -r requirements.txt 2>/dev/null || echo 'Usando dependências do sistema' && python3 bot_telegram.py"]
