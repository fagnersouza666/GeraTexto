#!/bin/bash

# Script simplificado para iniciar o GeraTexto Bot
echo "🤖 Iniciando GeraTexto Bot..."

# Verificar .env
if [ ! -f ".env" ]; then
    echo "❌ Configure o arquivo .env primeiro!"
    cp .env.example .env
    echo "📝 Arquivo .env criado. Configure suas chaves de API."
    exit 1
fi

# Parar e remover containers antigos
echo "🛑 Limpando containers antigos..."
docker-compose down --remove-orphans 2>/dev/null

# Iniciar com docker-compose
echo "🚀 Iniciando bot..."
docker-compose up -d

# Aguardar e verificar
echo "⏳ Aguardando inicialização (10s)..."
sleep 10

if docker-compose ps | grep -q "Up"; then
    echo "✅ Bot iniciado com sucesso!"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   Logs: docker logs -f geratexto-bot"
    echo "   Parar: docker-compose down"
    echo "   Status: docker-compose ps"
else
    echo "❌ Erro na inicialização"
    docker-compose ps
    echo "📋 Verifique: docker logs geratexto-bot"
fi 