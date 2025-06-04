FROM python:3.10-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Definir diretório de trabalho
WORKDIR /app

# Copiar apenas requirements.txt primeiro para aproveitar cache do Docker
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código
COPY . .

# Criar diretórios necessários
RUN mkdir -p posts templates

# Comando padrão
CMD ["python", "bot_telegram.py"]
