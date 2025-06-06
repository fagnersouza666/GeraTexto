#!/bin/bash
set -e

echo "🤖 Iniciando GeraTexto Bot..."

# Configurar variáveis de ambiente para Python
export PYTHONUNBUFFERED=1
export PYTHONDONTWRITEBYTECODE=1

# Aguardar estabilização da rede
echo "⏳ Aguardando estabilização da rede..."
sleep 10

# Tentar instalar dependências com retry
echo "📦 Instalando dependências..."
for i in {1..5}; do
    echo "Tentativa $i/5..."
    if pip install --no-cache-dir -r requirements.txt; then
        echo "✅ Dependências instaladas com sucesso!"
        break
    else
        echo "⚠️ Falha na tentativa $i"
        if [ $i -eq 5 ]; then
            echo "❌ Falha após 5 tentativas. Tentando continuar..."
        else
            sleep $((i * 5))  # Backoff exponencial
        fi
    fi
done

echo "🚀 Iniciando bot Telegram..."
echo "📋 Para parar: Ctrl+C ou docker stop geratexto-bot"
echo "📋 Para logs: docker logs -f geratexto-bot"
echo ""

exec python3 bot_telegram.py 