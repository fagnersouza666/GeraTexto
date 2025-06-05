#!/bin/bash

# Script para executar o GeraTexto via Docker
echo "🐳 Iniciando GeraTexto via Docker..."

# Verificar se o arquivo .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "📝 Criando arquivo .env de exemplo..."
    cp .env.example .env
    echo ""
    echo "🔧 Configure suas chaves de API no arquivo .env antes de continuar:"
    echo "   - TELEGRAM_TOKEN=seu_token_aqui"
    echo "   - OPENAI_API_KEY=sua_chave_aqui"
    echo "   - OPENAI_MODEL=gpt-4o-mini"
    echo ""
    echo "📋 Como obter as chaves:"
    echo "   🤖 Telegram: Fale com @BotFather e use /newbot"
    echo "   🧠 OpenAI: Acesse platform.openai.com → API Keys"
    echo ""
    echo "💡 Após configurar, execute novamente: ./run-docker.sh"
    exit 1
fi

# Verificar se as variáveis estão configuradas
source .env
if [ -z "$TELEGRAM_TOKEN" ] || [ -z "$OPENAI_API_KEY" ] || [ -z "$OPENAI_MODEL" ] || [ "$TELEGRAM_TOKEN" = "your_telegram_token_here" ] || [ "$OPENAI_API_KEY" = "your_openai_key_here" ]; then
    echo "❌ Configure as variáveis TELEGRAM_TOKEN, OPENAI_API_KEY e OPENAI_MODEL no arquivo .env"
    echo "💡 Edite o arquivo .env com suas chaves reais"
    echo ""
    echo "📋 Exemplo de configuração:"
    echo "   TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    echo "   OPENAI_API_KEY=sk-proj-abcd1234..."
    echo "   OPENAI_MODEL=gpt-4o-mini"
    exit 1
fi

echo "✅ Arquivo .env configurado"
echo "🤖 Usando modelo: $OPENAI_MODEL"

# Parar containers antigos se existirem
echo "🛑 Parando containers antigos..."
docker stop geratexto-bot 2>/dev/null || true
docker rm geratexto-bot 2>/dev/null || true

# Remover redes antigas se existirem
echo "🌐 Configurando rede Docker..."
docker network rm geratexto-network 2>/dev/null || true

# Construir a imagem
echo "🔨 Construindo imagem Docker..."
docker build -t geratexto . || {
    echo "❌ Erro ao construir imagem Docker"
    echo "💡 Tentando com docker-compose..."
    docker-compose down 2>/dev/null
    docker-compose up --build -d
    
    # Verificar se funcionou
    sleep 5
    if docker logs geratexto-bot 2>/dev/null | grep -q "✅ Dependências"; then
        echo "✅ GeraTexto iniciado via docker-compose!"
        echo ""
        echo "📋 Comandos úteis:"
        echo "   Ver logs:        docker logs -f geratexto-bot"
        echo "   Parar bot:       docker-compose down"
        echo "   Reiniciar bot:   docker-compose restart"
    else
        echo "❌ Problemas persistem. Verificar logs: docker logs geratexto-bot"
    fi
    exit $?
}

# Executar o container com configurações de DNS e rede
echo "🚀 Iniciando container com configurações de rede..."
docker run -d \
    --name geratexto-bot \
    --env-file .env \
    --restart unless-stopped \
    --dns 8.8.8.8 \
    --dns 8.8.4.4 \
    --dns 1.1.1.1 \
    --add-host api.telegram.org:149.154.167.220 \
    --add-host api.openai.com:104.18.7.192 \
    --sysctl net.ipv6.conf.all.disable_ipv6=1 \
    --network-mode bridge \
    -v "$(pwd)/posts:/app/posts" \
    -v "$(pwd)/templates:/app/templates" \
    geratexto

# Aguardar inicialização e verificar logs
sleep 5

if docker ps --filter name=geratexto-bot --filter status=running | grep -q geratexto-bot; then
    echo "✅ Container iniciado! Verificando conectividade..."
    
    # Verificar se as dependências foram instaladas
    if docker logs geratexto-bot 2>/dev/null | grep -q "✅ Dependências offline instaladas"; then
        echo "✅ Dependências instaladas com sucesso!"
        
        # Verificar se há erros de conectividade
        if docker logs geratexto-bot 2>/dev/null | grep -q "Temporary failure in name resolution"; then
            echo "⚠️ Ainda há problemas de DNS. Tentando docker-compose..."
            docker stop geratexto-bot
            docker rm geratexto-bot
            docker-compose up -d
        else
            echo "🎉 GeraTexto funcionando perfeitamente!"
        fi
    fi
    
    echo ""
    echo "🎉 Bot está rodando! Teste no Telegram:"
    echo "   /start - Inicializar o bot"
    echo "   /gerar <tema> - Gerar post sobre um tema"
    echo "   /tendencias - Ver tendências atuais"
    echo ""
    echo "📊 Status do container:"
    docker ps --filter name=geratexto-bot
    echo ""
    echo "📋 Comandos úteis:"
    echo "   Ver logs:        docker logs -f geratexto-bot"
    echo "   Parar bot:       docker stop geratexto-bot"
    echo "   Reiniciar bot:   docker restart geratexto-bot"
    echo "   Remover bot:     docker rm -f geratexto-bot"
    echo "   Teste DNS:       docker exec geratexto-bot nslookup google.com"
else
    echo "❌ Erro ao iniciar container"
    echo "📋 Tentando com docker-compose como fallback..."
    docker-compose down 2>/dev/null
    docker-compose up -d
    
    echo ""
    echo "📋 Para verificar logs e diagnóstico:"
    echo "   docker logs -f geratexto-bot"
    echo "   python verificar_conectividade.py"
fi 