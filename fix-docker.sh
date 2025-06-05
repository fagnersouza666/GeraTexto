#!/bin/bash

echo "🔧 Script de Correção: Erro ContainerConfig"
echo "==========================================="

echo "🛑 Parando containers..."
docker-compose down --remove-orphans

echo "🧹 Limpando sistema Docker..."
docker system prune -a -f --volumes

echo "🔨 Reconstruindo imagem..."
docker-compose build --no-cache

echo "🚀 Iniciando bot..."
docker-compose up -d

echo "⏳ Aguardando inicialização..."
sleep 10

echo "📋 Verificando status..."
docker-compose ps

echo "📄 Logs recentes:"
docker logs --tail 5 geratexto-bot

echo ""
echo "✅ Script de correção concluído!"
echo "Se o bot não iniciou, aguarde mais alguns segundos para instalação das dependências."
echo "Para monitorar: docker logs -f geratexto-bot" 