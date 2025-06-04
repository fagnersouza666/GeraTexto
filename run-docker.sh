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
if [ -z "$TELEGRAM_TOKEN" ] || [ -z "$OPENAI_API_KEY" ] || [ "$TELEGRAM_TOKEN" = "your_telegram_token_here" ] || [ "$OPENAI_API_KEY" = "your_openai_key_here" ]; then
    echo "❌ Configure as variáveis TELEGRAM_TOKEN e OPENAI_API_KEY no arquivo .env"
    echo "💡 Edite o arquivo .env com suas chaves reais"
    echo ""
    echo "📋 Exemplo de configuração:"
    echo "   TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
    echo "   OPENAI_API_KEY=sk-proj-abcd1234..."
    exit 1
fi

echo "✅ Arquivo .env configurado"

# Parar containers antigos se existirem
echo "🛑 Parando containers antigos..."
docker stop geratexto-bot 2>/dev/null || true
docker rm geratexto-bot 2>/dev/null || true

# Construir a imagem
echo "🔨 Construindo imagem Docker..."
docker build -t geratexto . || {
    echo "❌ Erro ao construir imagem Docker"
    echo "💡 Tentando com docker-compose..."
    docker-compose down 2>/dev/null
    docker-compose up --build -d
    exit $?
}

# Executar o container
echo "🚀 Iniciando container..."
docker run -d \
    --name geratexto-bot \
    --env-file .env \
    --restart unless-stopped \
    -v "$(pwd)/posts:/app/posts" \
    -v "$(pwd)/templates:/app/templates" \
    geratexto

if [ $? -eq 0 ]; then
    echo "✅ GeraTexto iniciado com sucesso!"
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
else
    echo "❌ Erro ao iniciar container"
    echo "📋 Tentando com docker-compose como fallback..."
    docker-compose up -d
fi 