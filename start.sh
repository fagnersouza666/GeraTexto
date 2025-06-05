#!/bin/bash
set -e

echo "🤖 Iniciando GeraTexto Bot..."

# Configurar variáveis de ambiente para Python
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Instalar dependências rapidamente
echo "📦 Instalando dependências..."
pip install --no-cache-dir -r requirements.txt > /dev/null 2>&1 || echo "⚠️ Usando dependências já disponíveis"

echo "✅ Dependências prontas!"

# Executar o bot diretamente
echo "🚀 Iniciando bot Telegram..."
echo "📋 Para parar: Ctrl+C ou docker stop geratexto-bot"
echo "📋 Para logs: docker logs -f geratexto-bot"
echo ""

exec python3 bot_telegram.py 