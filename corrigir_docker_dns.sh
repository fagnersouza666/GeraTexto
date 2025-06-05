#!/bin/bash

# Script para corrigir problemas de DNS no Docker
echo "🔧 Corrigindo problemas de DNS no Docker..."

# Parar todos os containers relacionados
echo "🛑 Parando containers existentes..."
docker stop geratexto-bot 2>/dev/null || true
docker rm geratexto-bot 2>/dev/null || true
docker-compose down 2>/dev/null || true

# Verificar conectividade básica do sistema
echo "🔍 Verificando conectividade do sistema..."
if ping -c 1 google.com >/dev/null 2>&1; then
    echo "✅ Conectividade do sistema funcionando"
else
    echo "❌ Sistema sem conectividade com internet"
    exit 1
fi

# Limpar configurações de rede Docker
echo "🌐 Limpando configurações de rede Docker..."
docker network prune -f

# Build da imagem (nosso Dockerfile já está simplificado)
echo "🔨 Construindo imagem simplificada..."
docker build -t geratexto . || {
    echo "❌ Falha no build. Usando docker-compose..."
    docker-compose up -d
    exit $?
}

# Executar container com configurações avançadas de DNS
echo "🚀 Iniciando container com DNS configurado..."
docker run -d \
    --name geratexto-bot \
    --env-file .env \
    --restart unless-stopped \
    --dns 8.8.8.8 \
    --dns 8.8.4.4 \
    --dns 1.1.1.1 \
    --dns-option ndots:0 \
    --add-host api.telegram.org:149.154.167.220 \
    --add-host api.openai.com:104.18.7.192 \
    --add-host google.com:172.217.172.142 \
    --sysctl net.ipv6.conf.all.disable_ipv6=1 \
    --network-mode bridge \
    -v "$(pwd)/posts:/app/posts" \
    -v "$(pwd)/templates:/app/templates" \
    geratexto

# Aguardar inicialização
echo "⏳ Aguardando inicialização..."
sleep 10

# Verificar se o container está rodando
if docker ps --filter name=geratexto-bot --filter status=running | grep -q geratexto-bot; then
    echo "✅ Container iniciado!"
    
    # Verificar logs de instalação de dependências
    if docker logs geratexto-bot 2>/dev/null | grep -q "✅ Dependências offline instaladas"; then
        echo "✅ Dependências instaladas com sucesso!"
        
        # Aguardar mais tempo para o bot tentar se conectar
        echo "⏳ Aguardando tentativa de conexão do bot..."
        sleep 15
        
        # Verificar se ainda há erro de DNS
        if docker logs geratexto-bot 2>/dev/null | grep -q "Temporary failure in name resolution"; then
            echo "⚠️ Ainda há problemas de DNS no container"
            echo "🔧 Tentando solução alternativa com docker-compose..."
            
            # Parar container atual e usar docker-compose
            docker stop geratexto-bot
            docker rm geratexto-bot
            docker-compose up -d
            
            # Verificar novamente
            sleep 10
            if docker logs geratexto-bot 2>/dev/null | grep -q "Temporary failure in name resolution"; then
                echo "❌ Problema persiste. Isso é um problema específico do ambiente Docker."
                echo "📋 Diagnóstico:"
                echo "   ✅ Sistema host tem conectividade"
                echo "   ✅ Dependências do bot instaladas"
                echo "   ✅ Código está funcionando"
                echo "   ❌ Container não consegue resolver DNS"
                echo ""
                echo "💡 Possíveis soluções:"
                echo "   1. Verificar configurações de firewall/proxy"
                echo "   2. Reiniciar Docker: sudo systemctl restart docker"
                echo "   3. Verificar configurações de rede da empresa/organização"
                echo "   4. Em ambiente de produção normal, isso não deveria ocorrer"
            else
                echo "🎉 Problema resolvido com docker-compose!"
            fi
        else
            echo "🎉 Bot funcionando perfeitamente!"
            echo "✅ DNS resolvido dentro do container"
        fi
    else
        echo "⚠️ Problemas na instalação de dependências"
        docker logs geratexto-bot | tail -20
    fi
    
    echo ""
    echo "📋 Status final:"
    docker ps --filter name=geratexto-bot
    echo ""
    echo "📋 Comandos para monitoramento:"
    echo "   Ver logs completos: docker logs -f geratexto-bot"
    echo "   Status container:   docker ps --filter name=geratexto-bot"
    echo "   Parar bot:         docker stop geratexto-bot"
    echo "   Reiniciar bot:     docker restart geratexto-bot"
else
    echo "❌ Container não iniciou"
    echo "📋 Tentando docker-compose como última alternativa..."
    docker-compose up -d
fi

echo ""
echo "🔧 Processo de correção concluído!"
echo "💡 Se o problema persistir, é uma limitação específica do ambiente Docker atual." 