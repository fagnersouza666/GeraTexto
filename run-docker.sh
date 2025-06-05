#!/bin/bash

# Script para executar o GeraTexto via Docker - Versão Corrigida
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
docker-compose down --remove-orphans 2>/dev/null || true

# Construir e iniciar com docker-compose (método que funciona 100%)
echo "🔨 Construindo e iniciando container..."
docker-compose up --build -d

# Aguardar inicialização
echo "⏳ Aguardando inicialização..."
sleep 8

# Verificar se está funcionando
if docker-compose ps | grep -q "Up"; then
    echo "✅ Container iniciado com sucesso!"
    
    # Aguardar mais um pouco para logs aparecerem
    sleep 5
    
    # Verificar logs para confirmar funcionamento
    echo "🔍 Verificando status..."
    if docker logs geratexto-bot 2>/dev/null | grep -q "Bot configurado com sucesso"; then
        echo "🎉 GeraTexto funcionando perfeitamente!"
        echo ""
        echo "🤖 Bot está rodando! Teste no Telegram:"
        echo "   /start - Inicializar o bot"
        echo "   /gerar <tema> - Gerar post sobre um tema"
        echo "   /tendencias - Ver tendências atuais"
        echo ""
    elif docker logs geratexto-bot 2>/dev/null | grep -q "Dependências.*instaladas"; then
        echo "✅ Bot ainda inicializando, aguarde mais alguns segundos..."
        echo "📋 Verifique os logs: docker logs -f geratexto-bot"
    else
        echo "⚠️ Bot iniciado, verificando logs..."
        echo "📋 Para diagnóstico: docker logs geratexto-bot"
    fi
    
    echo ""
    echo "📊 Status do container:"
    docker-compose ps
    echo ""
    echo "📋 Comandos úteis:"
    echo "   Ver logs:        docker logs -f geratexto-bot"
    echo "   Parar bot:       docker-compose down"
    echo "   Reiniciar bot:   docker-compose restart"
    echo "   Rebuild:         docker-compose up --build -d"
    
else
    echo "❌ Erro ao iniciar container"
    echo "📋 Verificando problemas..."
    docker-compose ps
    echo ""
    echo "📋 Para diagnóstico:"
    echo "   docker logs geratexto-bot"
    echo "   docker-compose logs"
    exit 1
fi 