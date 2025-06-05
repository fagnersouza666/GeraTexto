#!/bin/bash
set -e

echo "🤖 Iniciando GeraTexto Bot..."

# Configurar variáveis de ambiente para Python
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Verificar conectividade básica (não restritiva)
echo "🔍 Verificando conectividade básica..."
python3 verificar_conectividade.py || {
    echo "⚠️ Alguns problemas detectados, mas continuando..."
    echo "   O bot pode funcionar mesmo assim."
}

# Tentar instalar dependências offline primeiro
echo "📦 Verificando dependências offline..."
if [ -d "/app/docker-deps" ] && [ "$(ls -A /app/docker-deps 2>/dev/null)" ]; then
    echo "📦 Instalando dependências offline..."
    pip install --no-index --find-links /app/docker-deps /app/docker-deps/*.whl && echo "✅ Dependências offline instaladas" || echo "⚠️ Erro na instalação offline - tentando online"
else
    echo "⚠️ Dependências offline não encontradas"
fi

# Tentar instalar dependências online como fallback
echo "📦 Verificando dependências online..."
pip install --no-cache-dir -r requirements.txt 2>/dev/null && echo "✅ Dependências online verificadas" || echo "⚠️ Usando dependências já disponíveis"

# Aguardar um pouco antes de iniciar o bot
echo "⏳ Aguardando 3 segundos antes de iniciar..."
sleep 3

# Executar o bot com configurações otimizadas
echo "🚀 Iniciando bot Telegram..."
echo "📋 Para parar: Ctrl+C ou docker stop geratexto-bot"
echo "📋 Para logs: docker logs -f geratexto-bot"
echo ""

exec python3 bot_telegram.py 