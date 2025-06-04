# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [v2.0.0] - 2025-01-29 - Docker Exclusivo

### 🔄 **BREAKING CHANGES**
- **Execução exclusiva via Docker**: Removido suporte à instalação local
- Todos os scripts e funcionalidades agora são focados apenas em Docker

### ✅ Adicionado
- Script `run-docker.sh` para execução automatizada via Docker
- Validação automática de configurações no script de execução
- Fallback para docker-compose quando build direto falha
- Mapeamento de volumes para persistência de dados
- Comandos úteis para gerenciamento do container no README

### 🔧 Corrigido
- Dockerfile otimizado para usar dependências locais (.venv) quando disponível
- Melhor tratamento de erros no processo de build e execução
- Script de execução com verificações robustas de ambiente

### 📊 Melhorias
- README.md completamente reescrito focando apenas em Docker
- Documentação simplificada e mais objetiva
- Estrutura de projeto mais limpa
- Processo de setup reduzido a um único comando

### 🗑️ Removido
- `install.sh` (script de instalação local)
- `test_installation.py` (testes de instalação local)
- `Dockerfile.offline` (versão alternativa desnecessária)
- Documentação de instalação local
- Instruções de setup manual complexo

### ✅ Mantido
- Todas as funcionalidades do bot Telegram
- Configuração via arquivo `.env`
- Docker Compose como alternativa
- Estrutura de dependências em `requirements.txt`
- Funcionalidades de geração de texto, imagem e tendências

## [v1.2.0] - 2025-01-29 - Versão Híbrida

### ✅ Adicionado
- Script de instalação automática (`install.sh`)
- Sistema de testes de instalação (`test_installation.py`)
- Configuração Docker melhorada
- Dockerfile otimizado para builds mais eficientes
- Docker Compose para deployment simplificado
- Versões específicas nas dependências para maior estabilidade

### 🔧 Corrigido
- Problemas de build do Docker relacionados a network bridge
- Configuração de DNS no Docker daemon
- Verificação automática de dependências do sistema
- Criação automática de diretórios necessários

### 📊 Melhorias
- README.md detalhado com múltiplas opções de instalação
- Documentação de troubleshooting abrangente
- Processo de instalação mais robusto
- Compatibilidade melhorada com diferentes sistemas

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