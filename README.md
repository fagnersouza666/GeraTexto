# GeraTexto - Bot Telegram para Geração de Conteúdo

Bot do Telegram inteligente que utiliza IA para gerar posts automaticamente, criar imagens e obter tendências de pesquisa. **Execução exclusiva via Docker**.

## 🚀 Funcionalidades

- **Geração de Posts**: Cria conteúdo original utilizando OpenAI GPT
- **Imagens com IA**: Gera imagens relacionadas ao tema do post
- **Análise de Tendências**: Obtém tópicos em alta usando Google Trends
- **Bot Telegram**: Interface amigável através do Telegram
- **Templates Personalizáveis**: Sistema de templates para diferentes tipos de conteúdo

## 🐳 Execução via Docker

### Pré-requisitos

- **Docker** instalado e funcionando
- **Docker Compose** (opcional, incluído na maioria das instalações)

### Configuração Rápida

1. **Clone o repositório**:
   ```bash
   git clone <url-do-repositorio>
   cd GeraTexto
   ```

2. **Execute o script de inicialização**:
   ```bash
   ./run-docker.sh
   ```

O script automaticamente:
- Verifica se o arquivo `.env` existe
- Cria `.env` baseado no exemplo se necessário
- Valida as configurações
- Constrói a imagem Docker
- Inicia o container

### Configuração Manual

Se preferir configurar manualmente:

1. **Criar arquivo de configuração**:
   ```bash
   cp .env.example .env
   ```

2. **Editar variáveis de ambiente**:
   ```env
   TELEGRAM_TOKEN=seu_token_do_telegram_aqui
   OPENAI_API_KEY=sua_chave_openai_aqui
   ```

3. **Executar com Docker Compose**:
   ```bash
   docker-compose up --build -d
   ```

   **Ou Docker tradicional**:
   ```bash
   docker build -t geratexto .
   docker run -d --name geratexto-bot --env-file .env geratexto
   ```

## 🔧 Como Obter as Chaves de API

### Token do Telegram
1. Fale com [@BotFather](https://t.me/botfather) no Telegram
2. Use `/newbot` para criar um novo bot
3. Copie o token fornecido

### Chave da OpenAI
1. Acesse [platform.openai.com](https://platform.openai.com)
2. Crie uma conta e vá para API Keys
3. Gere uma nova chave secreta

## 📖 Como Usar

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

## 🛠️ Gerenciamento do Container

### Comandos Úteis

```bash
# Ver status
docker ps --filter name=geratexto-bot

# Ver logs em tempo real
docker logs -f geratexto-bot

# Parar o bot
docker stop geratexto-bot

# Reiniciar o bot
docker restart geratexto-bot

# Remover o container
docker rm -f geratexto-bot

# Usar docker-compose
docker-compose up -d     # Iniciar
docker-compose down      # Parar
docker-compose logs -f   # Ver logs
```

### Volumes Mapeados

O container mapeia os seguintes diretórios:
- `./posts` → `/app/posts` (posts gerados)
- `./templates` → `/app/templates` (templates personalizados)

## 🐛 Troubleshooting

### Problemas Comuns

1. **Container não inicia**:
   ```bash
   docker logs geratexto-bot
   ```

2. **Erro de variáveis de ambiente**:
   ```bash
   # Verificar .env
   cat .env
   # Reconfigurar se necessário
   cp .env.example .env
   ```

3. **Erro de build Docker**:
   ```bash
   # Limpar cache e tentar novamente
   docker system prune -f
   ./run-docker.sh
   ```

4. **Erro de permissões**:
   ```bash
   # Dar permissão ao script
   chmod +x run-docker.sh
   ```

## 📦 Estrutura do Projeto

```
GeraTexto/
├── 🐳 Dockerfile              # Configuração Docker
├── 🐳 docker-compose.yml      # Docker Compose
├── 🚀 run-docker.sh          # Script de execução
├── ⚙️  .env.example           # Exemplo de configuração
├── 📝 bot_telegram.py         # Bot principal
├── 🤖 escritor_ia.py          # Geração de texto
├── 🖼️  imagem_ia.py           # Geração de imagens
├── 📊 gerador_tendencias.py   # Análise de tendências
├── 🛠️  utils.py               # Utilitários
├── 📋 requirements.txt        # Dependências Python
└── 📁 posts/                  # Posts gerados (mapeado)
```

## 📝 Changelog / Atualizações Recentes

### [v2.0.0] - 2025-01-29

#### 🔄 Alterado
- **Execução exclusiva via Docker**: Removida instalação local
- Script `run-docker.sh` para facilitar execução
- Dockerfile otimizado para usar dependências locais
- README.md focado apenas em Docker

#### 🗑️ Removido
- `install.sh` (script de instalação local)
- `test_installation.py` (testes locais) 
- `Dockerfile.offline` (alternativa desnecessária)
- Suporte a execução local direta

#### ✅ Mantido
- Funcionalidades completas do bot
- Configuração via `.env`
- Docker Compose como alternativa
- Mapeamento de volumes para persistência

## 🔄 Versão Atual

**v2.0.0** - Execução exclusiva via Docker com script automatizado

## 📞 Suporte

Para problemas:

1. Execute `docker logs -f geratexto-bot` para ver os logs
2. Verifique se o arquivo `.env` está configurado corretamente
3. Use `./run-docker.sh` para reinicialização limpa
4. Consulte a seção de [Troubleshooting](#🐛-troubleshooting)

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

