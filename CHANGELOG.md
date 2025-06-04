# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [v1.2.0] - 2025-01-29

### ✅ Adicionado
- Script de instalação automática (`install.sh`) para facilitar setup
- Configuração Docker melhorada com DNS customizado
- Dockerfile otimizado para builds mais eficientes
- Docker Compose para deployment simplificado
- Versões específicas nas dependências para maior estabilidade
- Sistema de troubleshooting abrangente no README
- Arquivo `.dockerignore` otimizado
- Configuração de DNS no Docker daemon (`/etc/docker/daemon.json`)

### 🔧 Corrigido
- Problemas de build do Docker relacionados a network bridge
- Configuração de DNS no Docker daemon para resolver conectividade
- Verificação automática de dependências do sistema
- Criação automática de diretórios necessários (`posts`, `templates`)
- Compatibilidade com Python 3.10+ verificada automaticamente

### 📊 Melhorias
- README.md completamente reescrito e organizado
- Documentação de troubleshooting detalhada
- Processo de instalação mais robusto e confiável
- Compatibilidade melhorada com diferentes sistemas operacionais
- Estrutura de arquivos mais organizada
- Mensagens de erro mais claras e informativas

### 🔄 Alterado
- `requirements.txt` atualizado com versões específicas:
  - `python-telegram-bot==20.3`
  - `openai==1.3.8`
  - `requests==2.31.0`
  - `python-dotenv==1.0.0`
  - `pytrends==4.9.2`
  - `jinja2==3.1.2`
  - `Pillow==10.1.0`

## [v1.1.0] - Data anterior

### ✅ Adicionado
- Bot Telegram básico para geração de conteúdo
- Integração com OpenAI GPT para geração de texto
- Geração de imagens com IA
- Análise de tendências do Google Trends
- Sistema de templates com Jinja2
- Estrutura básica do projeto

### 🔧 Funcionalidades
- Comando `/start` para inicializar o bot
- Comando `/gerar <tema>` para criar posts
- Comando `/tendencias` para obter tópicos em alta
- Salvamento automático de posts gerados
- Interface de callback para adicionar imagens

## [v1.0.0] - Versão inicial

### ✅ Adicionado
- Estrutura inicial do projeto
- Configuração básica de dependências
- Licença MIT
- Arquivo README básico 