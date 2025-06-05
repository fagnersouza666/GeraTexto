# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [v2.1.1] - 2025-01-29

### ✨ Adicionado
- **Solução Docker offline completa**: Pasta `docker-deps/` com wheels Python 3.10 pré-baixadas
- **Script de inicialização robusto**: `start.sh` com instalação offline primeiro, fallback online
- **Dockerfile simplificado**: Sem comandos RUN que podem falhar por problemas de rede
- **Dependências compatíveis**: Wheels específicas para Python 3.10 (container)

### 🔄 Alterado
- **Processo de instalação**: Prioriza dependências offline, depois tenta online
- **Build Docker**: Extremamente simplificado, apenas copia arquivos
- **Documentação**: README atualizado com seção de solução de problemas Docker

### 🐛 Corrigido
- **Problemas de rede Docker**: Solução offline elimina dependência de conectividade durante build
- **Incompatibilidade de wheels**: Dependências baixadas especificamente para Python 3.10
- **Falhas de instalação**: Sistema de fallback garante que dependências sejam instaladas

### 📦 Dependências
- Todas as dependências principais incluídas offline: python-telegram-bot, openai, requests, etc.
- Dependências secundárias: pandas, numpy, lxml, pydantic, httpx, etc.
- Total: 32 wheels pré-baixadas para instalação offline

## [v2.1.0] - 2025-01-29

### ✨ Adicionado
- **Modelo OpenAI configurável**: Agora o modelo é definido via variável `OPENAI_MODEL` no arquivo `.env`
- Função `obter_modelo_openai()` em `utils.py` para centralizar a configuração
- Suporte para diferentes modelos: gpt-4o-mini (padrão), gpt-4o, gpt-3.5-turbo
- Validação da variável `OPENAI_MODEL` no script `run-docker.sh`

### 🔄 Alterado
- **API OpenAI atualizada**: Migração para a nova API da OpenAI (v1.3.8)
  - `escritor_ia.py`: Uso de `OpenAI()` client e `chat.completions.create()`
  - `imagem_ia.py`: Uso de `images.generate()` com modelo DALL-E 3
- **Dockerfile simplificado**: Instalação de dependências no runtime para evitar problemas de rede
- **Tamanho padrão de imagens**: Alterado para 1024x1024 pixels

### 🐛 Corrigido
- **Compatibilidade API**: Atualização para nova sintaxe da OpenAI
- **Configuração centralizada**: Modelo não mais hardcoded no código
- **Validação de ambiente**: Verificação da nova variável obrigatória

### 📝 Documentação
- README atualizado com informações sobre modelos disponíveis
- Exemplos de configuração do arquivo `.env`
- Seção sobre escolha de modelos OpenAI

## [v2.0.0] - 2025-01-28

### 🚀 Mudança Maior
- **Projeto exclusivamente Docker**: Removida instalação local, foco total em containers

### ✨ Adicionado
- **Script `run-docker.sh` completo**: Automação total com validação, build e execução
- **Validação automática de .env**: Criação e verificação de configurações
- **Instruções integradas**: Como obter tokens Telegram e OpenAI
- **Gerenciamento de containers**: Comandos para logs, restart, stop integrados
- **Fallback docker-compose**: Alternativa automática se build direto falhar

### ❌ Removido
- `install.sh`: Script de instalação local
- `test_installation.py`: Testes de instalação local
- `Dockerfile.offline`: Versão alternativa do Dockerfile

### 🔄 Alterado
- **Dockerfile otimizado**: Estrutura mais limpa e eficiente
- **README completamente reescrito**: Foco exclusivo em Docker
- **.dockerignore atualizado**: Exclusão de arquivos desnecessários

### 📝 Documentação
- Guia completo de uso Docker
- Troubleshooting para problemas comuns
- Comandos úteis para gerenciamento

## [v1.2.0] - 2025-01-27

### ✨ Adicionado
- **Dockerfile otimizado**: Configuração completa para containerização
- **Script install.sh**: Instalação local automatizada com verificações
- **Teste de instalação**: `test_installation.py` para validar dependências
- **docker-compose.yml**: Configuração completa com redes e volumes
- **Versionamento de dependências**: requirements.txt com versões fixas

### 🔄 Alterado
- **Estrutura do projeto**: Organização melhorada para Docker e local
- **Documentação expandida**: README com múltiplas opções de instalação
- **Configuração DNS Docker**: Tentativa de resolver problemas de rede

### 🐛 Corrigido
- **Dependências não versionadas**: Todas as dependências agora têm versões específicas
- **Problemas de build**: Múltiplas estratégias para diferentes ambientes

## [v1.1.0] - 2025-01-26

### ✨ Adicionado
- **Bot Telegram funcional**: Comandos básicos implementados
- **Geração de conteúdo**: Integração com OpenAI para posts
- **Geração de imagens**: Suporte a DALL-E para criação de imagens
- **Análise de tendências**: Google Trends integrado

### 🔄 Alterado
- **Estrutura modular**: Separação em módulos específicos
- **Sistema de templates**: Jinja2 para personalização de posts

## [v1.0.0] - 2025-01-25

### 🎉 Lançamento Inicial
- **Estrutura básica**: Configuração inicial do projeto
- **Dependências principais**: OpenAI, Telegram Bot, Google Trends
- **Configuração base**: Arquivos de configuração e estrutura de pastas 