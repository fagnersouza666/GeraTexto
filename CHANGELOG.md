# Changelog

Todas as mudanças importantes deste projeto serão documentadas neste arquivo.

## [2.1.0] - 2025-06-05

### ✅ Resolvido - Problemas de Conectividade
- **Sistema de retry robusto**: Implementado sistema de tentativas com backoff exponencial
- **Verificação de conectividade**: Teste automático de DNS e HTTP antes da inicialização
- **Network host**: Configuração para usar rede do host e evitar problemas de DNS no Docker
- **Healthcheck automático**: Sistema de monitoramento da saúde do container
- **Logs detalhados**: Sistema de logging melhorado para diagnóstico
- **Configuração simplificada**: Remoção de HTTPXRequest complexo, usando configuração padrão

### 🐛 Correções
- **Event loop**: Corrigido erro "Cannot close a running event loop" no Docker
- **DNS resolution**: Resolvido problema de resolução de nomes no container
- **Timeout issues**: Configurações de timeout otimizadas para ambientes com latência

### 🔧 Melhorias Técnicas
- **Função main_sync()**: Nova função síncrona para evitar conflitos de event loop
- **Verificação prévia**: Script `verificar_conectividade.py` melhorado
- **Healthcheck Docker**: Arquivo `healthcheck.py` para monitoramento automático
- **Container restart policy**: Política de reinicialização automática configurada

### 📊 Status Final
- ✅ Bot conectando com sucesso à API do Telegram
- ✅ Container com status "healthy"
- ✅ Polling de mensagens funcionando
- ✅ Todos os comandos operacionais

## [2.0.1] - 2025-06-05

### 🔧 Melhorias
- Adicionado sistema de dependências offline com 32 wheels pré-baixadas
- Script `start.sh` melhorado para instalação offline primeiro
- Configurações Docker otimizadas para ambiente offline
- DNS configurado com servidores Google (8.8.8.8, 8.8.4.4)

### 🐛 Correções
- Corrigido problema de ModuleNotFoundError com instalação offline
- Melhorado tratamento de erros durante instalação de dependências
- Script de verificação de conectividade aprimorado

## [2.0.0] - 2025-06-04

### 🚀 Nova Versão
- Migração para python-telegram-bot v20.3
- Interface completamente redesenhada com emojis e formatação
- Sistema de status e monitoramento implementado

### ✨ Novas Funcionalidades
- **Comando /status**: Verificação de status e uptime do bot
- **Interface melhorada**: Uso de emojis e formatação Markdown
- **Mensagens de processamento**: Feedback visual durante operações
- **Tratamento de erros**: Sistema robusto de tratamento de exceções

### 🎨 Melhorias de UX
- Botões interativos para geração de imagem
- Mensagens de feedback durante processamento
- Formatação melhorada dos posts e tendências
- Comandos mais intuitivos e informativos

### 🔧 Melhorias Técnicas
- **Async/await**: Migração completa para funções assíncronas
- **Error handling**: Tratamento de erros mais robusto
- **Logging**: Sistema de logs melhorado
- **Code organization**: Código mais organizado e modular

## [1.3.0] - 2025-06-03

### 🔧 Configuração
- Modelo OpenAI configurável via variável de ambiente OPENAI_MODEL
- Suporte para múltiplos modelos: gpt-4o-mini, gpt-4o, gpt-3.5-turbo
- Documentação atualizada com instruções de configuração

### 🐛 Correções
- Corrigido carregamento de variáveis de ambiente
- Melhorado tratamento de erros na geração de conteúdo
- Validação de configuração no startup

## [1.2.0] - 2025-06-02

### ✨ Funcionalidades
- Geração de imagens com DALL-E 3
- Sistema de templates Jinja2 para posts
- Análise de tendências Google Trends
- Sistema de callbacks para botões interativos

### 🔧 Melhorias
- Estrutura de arquivos organizada
- Sistema de logs implementado
- Validação de entrada do usuário
- Documentação expandida

## [1.1.0] - 2025-06-01

### ✨ Funcionalidades
- Bot básico do Telegram funcionando
- Comando /gerar para criação de posts
- Comando /tendencias para análise de tendências
- Integração com OpenAI GPT

### 🔧 Configuração
- Sistema de variáveis de ambiente
- Docker Compose configurado
- Estrutura básica do projeto

## [1.0.0] - 2025-05-31

### 🚀 Lançamento Inicial
- Projeto GeraTexto criado
- Estrutura básica implementada
- Configuração inicial do repositório
- Licença MIT adicionada

---

### Legenda
- 🚀 Nova versão maior
- ✨ Nova funcionalidade
- 🔧 Melhoria/atualização
- 🐛 Correção de bug
- 📊 Dados/métricas
- 🎨 Interface/UX
- 📝 Documentação
- ✅ Problema resolvido