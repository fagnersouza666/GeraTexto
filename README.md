# 🤖 GeraTexto Bot

**Bot Telegram para geração automatizada de conteúdo com IA**

Versão: **2.2.7** | Status: ✅ **Funcional** | Fontes: Reddit + TechCrunch + HackerNews

## 📋 Descrição

O GeraTexto Bot é um bot do Telegram que utiliza inteligência artificial para gerar posts criativos sobre qualquer tema. Com integração às principais APIs (OpenAI, Google Trends) e capacidade de gerar imagens com IA, o bot oferece uma solução completa para criação de conteúdo.

### ✨ Principais Recursos

- 🎯 **Geração de Posts**: Crie posts sobre qualquer tema usando IA
- 📈 **Tendências Inteligentes**: Clique em tendências do Reddit, TechCrunch e HackerNews
- 🧠 **Processamento Inteligente**: Sistema que extrai assuntos principais de tendências longas
- 🎨 **Imagens com IA**: Adicione imagens geradas por IA aos seus posts
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

### Usar Tendências Interativas
1. Digite `/tendencias`
2. Clique em qualquer botão de tendência
3. O bot gerará automaticamente um post sobre o tema

### Adicionar Imagem
Após gerar um post, clique no botão "🎨 Adicionar imagem IA" para criar uma imagem relacionada.

## 🛠️ Arquitetura Técnica

### Dependências Principais
- `python-telegram-bot==20.3` - Interface com Telegram
- `openai==1.3.8` - Geração de conteúdo e imagens
- `pytrends==4.9.2` - Obtenção de tendências do Google
- `jinja2==3.1.2` - Templates para posts
- `httpx==0.24.1` - Requisições HTTP robustas

### Estrutura do Projeto
```
GeraTexto/
├── bot_telegram.py          # Bot principal
├── escritor_ia.py           # Geração de posts com IA
├── imagem_ia.py            # Geração de imagens
├── gerador_tendencias.py   # Obtenção de tendências
├── utils.py                # Utilitários gerais
├── templates/              # Templates de posts
├── posts/                  # Posts gerados
├── docker-compose.yml      # Configuração Docker
└── requirements.txt        # Dependências Python
```

## 🔧 Resolução de Problemas

### Problemas de Conectividade
O bot inclui sistema robusto de conectividade com:
- Verificação DNS automática
- Retry automático em falhas
- Logs detalhados de diagnóstico
- Configuração de rede otimizada para Docker

### Logs e Monitoramento
```bash
# Ver logs em tempo real
docker logs -f geratexto-bot

# Verificar status do container
docker-compose ps

# Reiniciar se necessário
docker-compose restart
```

### Problemas Comuns

**Bot não responde:**
- Verifique se o token está correto no .env
- Confirme se o bot não está sendo usado em outro lugar
- Reinicie o container: `docker-compose restart`

**Erro ao gerar posts:**
- Verifique a chave da OpenAI no .env
- Confirme se há créditos na conta OpenAI
- Verifique logs: `docker logs geratexto-bot`

**Tendências não carregam:**
- O bot possui sistema de fallback automático
- Verifica múltiplas fontes (Google Trends, Reddit, HackerNews)
- Aguarde alguns segundos e tente novamente

## 📈 Monitoramento

### Healthcheck Automático
O bot inclui healthcheck que verifica:
- Conectividade com APIs
- Status das variáveis de ambiente
- Funcionamento geral do bot

### Métricas Disponíveis
- Status em tempo real via comando `/status`
- Logs estruturados com níveis de severidade
- Restart automático em caso de falhas

## 🔄 Atualizações Recentes

### Versão 2.2.7 (Atual)
- ✅ **Substituído**: Google Trends por TechCrunch RSS (mais confiável)
- ✅ **Adicionado**: Feed RSS do TechCrunch para tendências de tecnologia
- ✅ **Melhorado**: Mix de fontes: Reddit, TechCrunch e HackerNews
- ✅ **Corrigido**: Eliminados erros 404 do Google Trends
- ✅ **Expandido**: Mais temas de fallback relacionados à tecnologia

## 📋 Dependências

### Sistema
- Docker 20.10+
- Docker Compose 2.0+
- Conexão com internet

### APIs Externas
- Telegram Bot API
- OpenAI API (GPT + DALL-E)
- Google Trends (opcional)

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Faça push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Desenvolvido com ❤️ para automatizar a criação de conteúdo**

Para suporte ou dúvidas, abra uma issue no repositório.

