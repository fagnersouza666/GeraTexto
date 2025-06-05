#!/bin/bash

echo "🤖 Iniciando GeraTexto Bot..."

# Tentar instalar dependências offline primeiro
echo "📦 Verificando dependências offline..."
if [ -d "/app/docker-deps" ]; then
    echo "📦 Instalando dependências offline..."
    pip install --no-index --find-links /app/docker-deps /app/docker-deps/*.whl && echo "✅ Dependências offline instaladas" || echo "⚠️  Erro na instalação offline"
fi

# Tentar instalar dependências online como fallback
echo "📦 Verificando dependências online..."
pip install --no-cache-dir python-telegram-bot==20.3 openai==1.3.8 requests==2.31.0 python-dotenv==1.0.0 pytrends==4.9.2 jinja2==3.1.2 Pillow==10.1.0 2>/dev/null && echo "✅ Dependências online instaladas" || echo "⚠️  Usando dependências já disponíveis"

# Executar o bot
echo "🚀 Iniciando bot Telegram..."
exec python3 bot_telegram.py 