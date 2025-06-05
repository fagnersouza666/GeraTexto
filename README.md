# 🤖 GeraTexto Bot

Bot Telegram inteligente para geração automática de conteúdo usando IA. Cria posts personalizados, gera imagens com DALL-E e acompanha tendências atuais.

## ✨ Funcionalidades

- 📝 **Geração de Posts**: Criação de conteúdo personalizado via IA
- 🎨 **Geração de Imagens**: Criação de imagens com DALL-E
- 📈 **Tendências**: Acompanhamento de tópicos em alta
- 🔍 **Status**: Monitoramento do status do bot
- 🐳 **Dockerizado**: Execução robusta com Docker

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- Tokens de API do Telegram e OpenAI

### 1. Clone o Repositório

```bash
git clone <url-do-repositorio>
cd GeraTexto
```

### 2. Configure as Variáveis de Ambiente

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais:

```env
TELEGRAM_TOKEN=seu_token_telegram
OPENAI_API_KEY=sua_chave_openai
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. Execução Local (Desenvolvimento)

```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar bot
python bot_telegram.py
```

### 4. Execução com Docker (Produção)

```bash
# Construir e executar
docker build -t geratexto-bot .
docker run -d --name geratexto-bot \
  --restart unless-stopped \
  --network host \
  --env-file .env \
  -v $(pwd)/posts:/app/posts \
  -v $(pwd)/templates:/app/templates \
  geratexto-bot
```

## 📋 Comandos do Bot

- `/start` - Inicializar o bot e ver comandos disponíveis
- `/gerar <tema>` - Gerar post sobre um tema específico
- `/tendencias` - Ver tendências atuais do Google Trends
- `/status` - Verificar status e uptime do bot

## 🔧 Arquitetura

### Componentes Principais

- **`bot_telegram.py`** - Bot principal com handlers Telegram
- **`escritor_ia.py`** - Geração de texto com OpenAI
- **`imagem_ia.py`** - Geração de imagens com DALL-E
- **`gerador_tendencias.py`** - Busca de tendências Google Trends
- **`healthcheck.py`** - Verificação de saúde do container
- **`verificar_conectividade.py`** - Diagnóstico de conectividade

### Melhorias de Conectividade

- ✅ **Sistema de Retry**: Tentativas automáticas com backoff exponencial
- ✅ **Verificação DNS**: Resolução de nomes antes da inicialização
- ✅ **Healthcheck**: Monitoramento automático da saúde do container
- ✅ **Network Host**: Uso da rede do host para evitar problemas de DNS
- ✅ **Configuração Robusta**: Timeouts e configurações otimizadas

## 🐛 Solução de Problemas

### Problemas de Conectividade

Se o bot não conseguir conectar:

1. **Verificar conectividade**:
   ```bash
   python verificar_conectividade.py
   ```

2. **Verificar logs do container**:
   ```bash
   docker logs geratexto-bot
   ```

3. **Reiniciar serviços Docker**:
   ```bash
   sudo systemctl restart docker
   ```

### Problemas de DNS

- O bot usa automaticamente `--network host` para evitar problemas de DNS
- Servidores DNS configurados: 8.8.8.8, 8.8.4.4, 1.1.1.1
- Hosts mapeados para APIs principais

## 📊 Monitoramento

### Healthcheck

O container inclui healthcheck automático que verifica:
- Resolução DNS
- Conectividade HTTP
- Status do bot Telegram

### Logs

```bash
# Ver logs em tempo real
docker logs -f geratexto-bot

# Ver últimas 50 linhas
docker logs geratexto-bot --tail 50
```

## 🔄 Dependências

```
python-telegram-bot==20.3  # API Telegram
openai==1.3.8             # API OpenAI
requests==2.31.0          # HTTP requests
python-dotenv==1.0.0      # Variáveis ambiente
pytrends==4.9.2           # Google Trends
jinja2==3.1.2             # Templates
Pillow==10.1.0            # Processamento imagem
httpx==0.24.1             # Cliente HTTP async
```

## 📝 Estrutura de Arquivos

```
GeraTexto/
├── bot_telegram.py         # Bot principal
├── escritor_ia.py          # Geração de texto
├── imagem_ia.py           # Geração de imagem
├── gerador_tendencias.py  # Tendências
├── healthcheck.py         # Healthcheck
├── verificar_conectividade.py # Diagnóstico
├── utils.py               # Utilitários
├── requirements.txt       # Dependências Python
├── Dockerfile            # Configuração Docker
├── start.sh             # Script inicialização
├── .env.example         # Exemplo variáveis
├── posts/               # Posts gerados
├── templates/           # Templates HTML
└── docker-deps/         # Dependências offline
```

## 🔒 Segurança

- ✅ Variáveis de ambiente para credenciais
- ✅ Não exposição de tokens nos logs
- ✅ Validação de entrada do usuário
- ✅ Tratamento de erros robusto

## 📈 Changelog / Atualizações Recentes

### v2.1.0 (2025-06-05)
- ✅ **Resolução de conectividade**: Sistema robusto de retry e backoff exponencial
- ✅ **Healthcheck Docker**: Monitoramento automático da saúde do container
- ✅ **Network Host**: Uso da rede do host para resolver problemas de DNS
- ✅ **Verificação DNS**: Teste de conectividade antes da inicialização
- ✅ **Logs melhorados**: Sistema de logging mais detalhado
- ✅ **Configuração simplificada**: Remoção de configurações complexas desnecessárias

### v2.0.0 (2025-06-05)
- 🔄 Migração para python-telegram-bot v20.3
- 🎨 Interface melhorada com emojis e formatação
- 📊 Sistema de status e monitoramento

## 🆔 Versão Atual

**v2.1.0** - Bot de geração de conteúdo com conectividade robusta

---

💡 **Desenvolvido com foco em estabilidade e conectividade confiável**

