#!/bin/bash

echo "�� Script de Correção Avançado: Problemas de Conectividade"
echo "=========================================================="

echo "🛑 Parando containers e serviços..."
docker-compose down --remove-orphans
docker stop $(docker ps -aq) 2>/dev/null || true

echo "🧹 Limpeza completa do Docker..."
docker system prune -a -f --volumes
docker network prune -f
docker volume prune -f

echo "🌐 Verificando e corrigindo DNS do sistema..."
# Flush DNS cache
sudo systemctl restart systemd-resolved 2>/dev/null || true
sudo systemctl flush-dns 2>/dev/null || true

# Testar DNS básico
echo "🔍 Testando conectividade DNS..."
nslookup api.telegram.org 8.8.8.8 || echo "⚠️ DNS pode ter problemas"
nslookup api.openai.com 8.8.8.8 || echo "⚠️ DNS pode ter problemas"

echo "🔨 Reconstruindo imagem (sem cache)..."
docker-compose build --no-cache --pull

echo "🚀 Iniciando bot com configurações DNS melhoradas..."
docker-compose up -d

echo "⏳ Aguardando inicialização (30s)..."
sleep 30

echo "📋 Verificando status do container..."
docker-compose ps

echo "📄 Logs dos últimos 10 segundos:"
docker logs --since 10s geratexto-bot

echo ""
echo "✅ Script de correção avançado concluído!"
echo "📊 Para monitorar em tempo real: docker logs -f geratexto-bot"
echo "🔄 Se ainda houver problemas, aguarde mais 1-2 minutos para estabilização" 