#!/bin/bash

echo "🤖 GeraTexto Bot - Execução Local"
echo "================================="

# Verificar se o ambiente virtual existe
if [[ ! -d ".venv" ]]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "Execute: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Ativar ambiente virtual
source .venv/bin/activate

# Verificar dependências
echo "📦 Verificando dependências..."
pip install --no-cache-dir -r requirements.txt > /dev/null 2>&1

# Verificar variáveis de ambiente
if [[ ! -f ".env" ]]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "Copie .env.example para .env e configure as variáveis"
    exit 1
fi

# Carregar variáveis de ambiente
source .env

if [[ -z "$TELEGRAM_TOKEN" || -z "$OPENAI_API_KEY" ]]; then
    echo "❌ Variáveis de ambiente não configuradas!"
    echo "Configure TELEGRAM_TOKEN e OPENAI_API_KEY no arquivo .env"
    exit 1
fi

echo "✅ Configuração verificada!"
echo "🚀 Iniciando GeraTexto Bot..."
echo ""
echo "📋 Para parar: Ctrl+C"
echo "📋 Logs serão exibidos abaixo:"
echo ""

# Executar bot com logs
python bot_telegram.py 