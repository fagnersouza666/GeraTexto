#!/bin/bash
set -e

echo "🤖 Iniciando GeraTexto Bot..."

# Configurar variáveis de ambiente para Python
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Verificar conectividade básica
echo "🔍 Verificando conectividade básica..."
python3 verificar_conectividade.py || {
    echo "⚠️ Problemas de conectividade detectados, mas continuando..."
}

# Tentar instalar dependências offline primeiro
echo "📦 Verificando dependências offline..."
if [ -d "/app/docker-deps" ]; then
    echo "📦 Instalando dependências offline..."
    pip install --no-index --find-links /app/docker-deps /app/docker-deps/*.whl && echo "✅ Dependências offline instaladas" || echo "⚠️ Erro na instalação offline"
fi

# Tentar instalar dependências online como fallback
echo "📦 Verificando dependências online..."
pip install --no-cache-dir -r requirements.txt 2>/dev/null && echo "✅ Dependências online instaladas" || echo "⚠️ Usando dependências já disponíveis"

# Aguardar um pouco antes de iniciar o bot
echo "⏳ Aguardando 5 segundos antes de iniciar..."
sleep 5

# Executar o bot com configurações otimizadas
echo "🚀 Iniciando bot Telegram..."
exec python3 bot_telegram.py 