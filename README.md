# 🤖 GeraTexto Bot

**Bot Telegram para geração automatizada de conteúdo com IA**

Versão: **2.2.9** | Status: ✅ **Funcional** | Anexos: ✅ **Arquivos .txt enviados automaticamente** | Fontes: Reddit + TechCrunch + HackerNews

## 📋 Descrição

O GeraTexto Bot é um bot do Telegram que utiliza inteligência artificial para gerar posts criativos sobre qualquer tema. Com integração às principais APIs (OpenAI, Google Trends) e capacidade de gerar imagens com IA, o bot oferece uma solução completa para criação de conteúdo.

### ✨ Principais Recursos

- 🎯 **Geração de Posts**: Crie posts sobre qualquer tema usando IA
- 📈 **Tendências Inteligentes**: Clique em tendências do Reddit, TechCrunch e HackerNews
- 🧠 **Processamento Inteligente**: Sistema que extrai assuntos principais de tendências longas
- 🎨 **Imagens com IA**: Adicione imagens geradas por IA aos seus posts
- 📎 **Anexos Automáticos**: Arquivos .txt enviados automaticamente como anexo no Telegram
- 💾 **Salvamento Automático**: Posts salvos automaticamente em arquivos
- 🔄 **Sistema Robusto**: Reconexão automática e tratamento de erros
- 🐳 **Containerizado**: Execução simplificada com Docker

## 🚀 Instalação e Configuração

### Pré-requisitos

- Docker e Docker Compose
- Chaves de API:
  - Token do Bot Telegram (via @BotFather)
  - Chave da API OpenAI

### ⚡ Configuração Rápida (Recomendado)

1. **Clone o repositório:**
```bash
git clone <repositorio>
cd GeraTexto
```

2. **Configure as variáveis de ambiente:**
```bash
cp .env.example .env
# Edite o arquivo .env com suas chaves
```

3. **Inicie o bot (método mais simples):**
```bash
./start-bot.sh
```

**OU use o script completo:**
```bash
./run-docker.sh
```

**OU use docker-compose diretamente:**
```bash
docker-compose up -d
```

4. **Verifique os logs:**
```bash
docker logs -f geratexto-bot
```

### 📋 Scripts Disponíveis

- **`./start-bot.sh`** - Script simplificado que sempre funciona ✅
- **`./run-docker.sh`** - Script completo com validações
- **`docker-compose up -d`** - Comando direto do Docker Compose

### Arquivo .env

```env
TELEGRAM_TOKEN=seu_token_aqui
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_IMAGE_MODEL=dall-e-3
```

## 📱 Comandos Disponíveis

- `/start` - Inicializar o bot e ver comandos
- `/gerar <tema>` - Gerar post sobre um tema específico
- `/tendencias` - Ver tendências atuais com botões interativos
- `/status` - Verificar status e conectividade do bot

## 🎯 Exemplos de Uso

### Gerar Post Manualmente
```
/gerar Inteligência Artificial no futuro
```
O bot enviará o post completo e automaticamente um arquivo .txt como anexo para fácil cópia.

### Usar Tendências Interativas
1. Digite `/tendencias`
2. Clique em qualquer botão de tendência
3. O bot gerará automaticamente um post sobre o tema
4. Arquivo .txt será enviado como anexo automaticamente

### Adicionar Imagem
Após gerar um post, clique no botão "🎨 Adicionar imagem IA" para criar uma imagem relacionada.
O arquivo .txt também será reenviado como anexo junto com a imagem.

## 🛠️ Arquitetura Técnica

### Dependências Principais
- `python-telegram-bot==20.3` - Interface com Telegram
- `openai==1.3.8` - Geração de conteúdo e imagens
- `pytrends==4.9.2` - Obtenção de tendências do Google
- `jinja2==3.1.2` - Templates para posts
- `httpx==0.24.1`