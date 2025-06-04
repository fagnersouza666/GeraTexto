#!/bin/bash

# Script de instalação do GeraTexto
echo "=== Instalação do GeraTexto ==="

# Verificar se Python 3.10+ está instalado
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10.0"

if ! python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "❌ Python 3.10+ é necessário. Versão atual: $python_version"
    exit 1
fi

echo "✅ Python $python_version encontrado"

# Criar e ativar ambiente virtual
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
fi

echo "🔧 Ativando ambiente virtual..."
source .venv/bin/activate

echo "📥 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Criar diretórios necessários
mkdir -p posts templates

# Verificar arquivo .env
if [ ! -f ".env" ]; then
    echo "⚠️  Arquivo .env não encontrado. Copiando exemplo..."
    cp .env.example .env
    echo "📝 Edite o arquivo .env com suas chaves de API antes de executar o bot"
fi

echo "✅ Instalação concluída!"

# Executar testes de verificação
echo ""
echo "🧪 Executando testes de verificação..."
python test_installation.py

echo ""
echo "📋 Próximos passos:"
echo "1. Edite o arquivo .env com suas chaves de API"
echo "2. Execute: source .venv/bin/activate"
echo "3. Execute: python bot_telegram.py"
echo ""
echo "💡 Para executar com Docker (se disponível):"
echo "   docker-compose up --build" 