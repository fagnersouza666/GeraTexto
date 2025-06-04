FROM python:3.10-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Definir diretório de trabalho
WORKDIR /app

# Copiar todo o projeto incluindo venv se existir
COPY . .

# Se .venv existe, copiar as dependências instaladas localmente
RUN if [ -d ".venv" ]; then \
    pip install --upgrade pip && \
    cp -r .venv/lib/python*/site-packages/* /usr/local/lib/python3.10/site-packages/; \
    else \
    pip install --upgrade pip && \
    pip install python-telegram-bot==20.3 openai==1.3.8 requests==2.31.0 python-dotenv==1.0.0 pytrends==4.9.2 jinja2==3.1.2 Pillow==10.1.0; \
    fi

# Criar diretórios necessários
RUN mkdir -p posts templates

# Comando padrão
CMD ["python", "bot_telegram.py"]
