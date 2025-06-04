# GeraTexto - Bot Telegram para Geração de Conteúdo

Um bot do Telegram inteligente que utiliza IA para gerar posts automaticamente, criar imagens e obter tendências de pesquisa para criação de conteúdo engajante.

## 🚀 Funcionalidades

- **Geração de Posts**: Cria conteúdo original utilizando OpenAI GPT
- **Imagens com IA**: Gera imagens relacionadas ao tema do post
- **Análise de Tendências**: Obtém tópicos em alta usando Google Trends
- **Bot Telegram**: Interface amigável através do Telegram
- **Templates Personalizáveis**: Sistema de templates para diferentes tipos de conteúdo

## 📋 Instruções de Instalação

### Opção 1: Instalação Automática (Recomendada)

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd GeraTexto

# Execute o script de instalação
chmod +x install.sh
./install.sh
```

### Opção 2: Instalação Manual

```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Criar diretórios necessários
mkdir -p posts templates

# Configurar variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas chaves de API
```

### Opção 3: Docker (Se disponível)

```bash
# Usar docker-compose
docker-compose up --build

# Ou build manual
docker build -t geratexto .
docker run -d --env-file .env geratexto
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```env
TELEGRAM_TOKEN=seu_token_do_telegram_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
```

### Como Obter as Chaves

1. **Token do Telegram**:
   - Fale com [@BotFather](https://t.me/botfather) no Telegram
   - Use `/newbot` para criar um novo bot
   - Copie o token fornecido

2. **Chave da OpenAI**:
   - Acesse [platform.openai.com](https://platform.openai.com)
   - Crie uma conta e vá para API Keys
   - Gere uma nova chave secreta

## 📖 Exemplos de Uso

### Comandos do Bot

```
/start - Inicializar o bot
/gerar <tema> - Gerar post sobre um tema específico
/tendencias - Obter tendências atuais do Google
```

### Exemplo de Uso

```
/gerar inteligência artificial

# O bot irá:
# 1. Gerar um post completo sobre IA
# 2. Oferecer opção para adicionar imagem
# 3. Salvar o conteúdo em arquivo
```

## 📦 Dependências

### Principais

- **python-telegram-bot==20.3** - API do Telegram
- **openai==1.3.8** - API da OpenAI
- **requests==2.31.0** - Requisições HTTP
- **python-dotenv==1.0.0** - Gerenciamento de variáveis de ambiente
- **pytrends==4.9.2** - Google Trends API
- **jinja2==3.1.2** - Sistema de templates
- **Pillow==10.1.0** - Processamento de imagens

### Compatibilidade

- **Python**: 3.10 ou superior
- **Sistema Operacional**: Linux, macOS, Windows
- **Docker**: Opcional (versão 20.10+)

## 🐛 Troubleshooting

### Problemas Comuns

1. **Erro de instalação Docker**:
   ```bash
   # Use a instalação local
   ./install.sh
   ```

2. **Erro "network bridge not found"**:
   ```bash
   # Reinicie o Docker
   sudo systemctl restart docker
   
   # Ou use a instalação local
   ./install.sh
   ```

3. **Erro de dependências**:
   ```bash
   # Limpe o cache e reinstale
   pip cache purge
   pip install --force-reinstall -r requirements.txt
   ```

4. **Erro de variáveis de ambiente**:
   ```bash
   # Verifique se o arquivo .env existe e tem as chaves corretas
   cat .env
   ```

## 📝 Changelog / Atualizações Recentes

### [v1.2.0] - 2025-01-29

#### ✅ Adicionado
- Script de instalação automática (`install.sh`)
- Configuração Docker melhorada com DNS customizado
- Dockerfile otimizado para builds mais eficientes
- Docker Compose para deployment simplificado
- Versões específicas nas dependências para maior estabilidade
- Sistema de troubleshooting abrangente

#### 🔧 Corrigido
- Problemas de build do Docker relacionados a network bridge
- Configuração de DNS no Docker daemon
- Verificação automática de dependências do sistema
- Criação automática de diretórios necessários

#### 📊 Melhorias
- README.md mais detalhado e organizado
- Documentação de troubleshooting
- Processo de instalação mais robusto
- Compatibilidade melhorada com diferentes sistemas

## 🔄 Versão Atual

**v1.2.0** - Sistema de geração de conteúdo com IA otimizado e instalação simplificada

## 📞 Suporte

Para problemas ou dúvidas:

1. Verifique a seção de [Troubleshooting](#🐛-troubleshooting)
2. Consulte o arquivo `CHANGELOG.md` para atualizações recentes
3. Execute `./install.sh` para reinstalação limpa
4. Verifique os logs: `tail -f logs/bot.log` (se disponível)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

