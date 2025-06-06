#!/bin/bash

echo "🐳 GeraTexto Bot - Docker"
echo "========================="

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Copie .env.example para .env e configure suas chaves:"
    echo "   cp .env.example .env"
    echo "   nano .env"
    exit 1
fi

# Verificar se Docker está rodando
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker não está rodando!"
    echo "🚀 Inicie o Docker e tente novamente"
    exit 1
fi

echo "✅ Iniciando GeraTexto Bot com Docker..."
docker-compose up -d

echo ""
echo "🎉 Bot iniciado com sucesso!"
echo "📊 Para ver logs: docker logs -f geratexto-bot"
echo "⏹️ Para parar: docker-compose down"
echo "📋 Para status: docker-compose ps" 