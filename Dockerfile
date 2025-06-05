FROM python:3.10-slim

# Configurar variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos do projeto
COPY . .

# Tornar start.sh executável (feito na cópia, não via RUN)
# Comando de execução que já instala dependências offline
CMD ["./start.sh"]
