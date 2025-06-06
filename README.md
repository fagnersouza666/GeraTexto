# GeraTexto Bot 🤖

**Versão 2.5.0** - Bot Telegram inteligente para geração de conteúdo com IA

## 🚀 Recursos Principais

- **📝 Geração de Posts**: Cria conteúdo sobre qualquer tema
- **🌐 Processamento de URLs**: Extrai e resume conteúdo de páginas web
- **📈 Tendências Automáticas**: Reddit + TechCrunch + HackerNews
- **🎨 Imagens com IA**: DALL-E integrado 
- **📎 Anexos Automáticos**: Arquivos .txt para cópia fácil
- **💾 Preservação de Conteúdo**: Texto original mantido ao gerar imagens

## 🐳 Instalação e Execução com Docker

### Pré-requisitos
- Docker e Docker Compose instalados
- Chaves de API (Telegram e OpenAI)

### 🚀 Instalação Rápida

```bash
# 1. Clonar repositório
git clone <repository-url>
cd GeraTexto

# 2. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves API

# 3. Iniciar com Docker
docker-compose up -d

# 4. Verificar status
docker-compose ps
docker logs -f geratexto-bot
```

### ⚙️ Configuração

Crie o arquivo `.env` com suas chaves:

```env
TELEGRAM_TOKEN=seu_token_telegram
OPENAI_API_KEY=sua_chave_openai
OPENAI_MODEL=gpt-4o-mini
```

### Como Obter as Chaves:

1. **Telegram Token**: 
   - Acesse @BotFather no Telegram
   - Digite `/newbot` e siga as instruções
   - Copie o token fornecido

2. **OpenAI API Key**: 
   - Acesse [platform.openai.com](https://platform.openai.com)
   - Vá em API Keys > Create new secret key
   - Copie a chave gerada

## 📋 Comandos do Bot

- `/start` - Inicializar bot
- `/gerar <tema>` - Criar post sobre tema
- `/gerar <URL>` - Extrair e criar post de URL
- `/tendencias` - Ver tendências atuais  
- `/status` - Verificar status do bot

## 💡 Exemplos de Uso

```
/gerar Inteligência Artificial em 2024
/gerar https://techcrunch.com/artigo-exemplo
/tendencias
```

## 🔧 Comandos Docker Úteis

### Gerenciamento Básico
```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Rebuild completo
docker-compose up --build

# Ver logs em tempo real
docker logs -f geratexto-bot

# Ver status
docker-compose ps
```

### Debugging e Manutenção
```bash
# Acessar shell do container
docker exec -it geratexto-bot bash

# Verificar conectividade
docker exec geratexto-bot python3 verificar_conectividade.py

# Restart rápido
docker restart geratexto-bot

# Limpar cache e rebuild
docker-compose down
docker system prune -f
docker-compose up --build
```

## 🛠️ Troubleshooting

### ❌ Container não inicia
```bash
# Verificar logs de erro
docker logs geratexto-bot

# Rebuild completo
docker-compose down
docker-compose up --build

# Verificar .env
cat .env
```

### ❌ Problemas de conectividade
```bash
# Testar conectividade dentro do container
docker exec geratexto-bot python3 verificar_conectividade.py

# Verificar se o network_mode está funcionando
docker exec geratexto-bot ping 8.8.8.8
```

### ❌ Bot não responde no Telegram
- Verifique se o TELEGRAM_TOKEN está correto no .env
- Confirme se o bot foi criado corretamente via @BotFather
- Verifique logs: `docker logs -f geratexto-bot`

### ❌ Erro de API OpenAI
- Verifique se OPENAI_API_KEY está correta no .env
- Confirme se há créditos na conta OpenAI
- Teste com modelo diferente (ex: gpt-3.5-turbo)

## 📁 Estrutura do Projeto

```
GeraTexto/
├── docker-compose.yml      # 🐳 Configuração Docker
├── Dockerfile              # 🐳 Imagem Docker
├── start.sh                # 🚀 Script de inicialização
├── bot_telegram.py         # 🤖 Bot principal
├── escritor_ia.py          # ✍️ Geração de textos
├── imagem_ia.py           # 🎨 Geração de imagens
├── gerador_tendencias.py  # 📈 Captação de tendências
├── healthcheck.py         # 🏥 Verificação de saúde
├── verificar_conectividade.py # 🌐 Teste de conectividade
├── posts/                 # 📄 Posts gerados
├── templates/             # 📋 Templates
└── tests/                 # 🧪 Testes unitários
```

## 🧪 Executar Testes

```bash
# Executar testes dentro do container
docker exec geratexto-bot python -m pytest

# Teste específico
docker exec geratexto-bot python -m pytest tests/test_escritor.py -v

# Com coverage
docker exec geratexto-bot python -m pytest --cov=. tests/
```

## 📊 Monitoramento

### Logs em Tempo Real
```bash
# Logs completos
docker logs -f geratexto-bot

# Apenas últimas 50 linhas
docker logs --tail 50 geratexto-bot

# Logs com timestamp
docker logs -t geratexto-bot
```

### Status e Performance
```bash
# Status do container
docker stats geratexto-bot

# Informações do container
docker inspect geratexto-bot

# Uso de recursos
docker exec geratexto-bot top
```

## 🔄 Atualização

Para atualizar o bot:

```bash
# 1. Parar container
docker-compose down

# 2. Atualizar código
git pull

# 3. Rebuild e reiniciar
docker-compose up --build -d

# 4. Verificar funcionamento
docker logs -f geratexto-bot
```

## 🚨 Backup e Restauração

### Backup dos Dados
```bash
# Backup da pasta posts
docker cp geratexto-bot:/app/posts ./backup-posts-$(date +%Y%m%d)

# Backup completo
tar -czf backup-geratexto-$(date +%Y%m%d).tar.gz posts/ templates/ .env
```

### Restauração
```bash
# Restaurar posts
docker cp ./backup-posts-YYYYMMDD geratexto-bot:/app/posts

# Restart após restauração
docker restart geratexto-bot
```

## 🔄 Atualizações Recentes (v2.5.0)

- ✅ **Nova Funcionalidade**: Clique em tendência agora extrai e analisa conteúdo da URL
- ✅ **Posts Mais Ricos**: Baseados no conteúdo real da página, não apenas no título  
- ✅ **Message_too_long RESOLVIDO**: Validação automática e truncamento inteligente
- ✅ **Melhor Estabilidade**: Error handling robusto e prevenção de erros em cascata
- ✅ **Prompts Otimizados**: Limitação de tamanho para evitar mensagens muito longas

## 🔄 Versão Anterior (v2.4.0)

- ✅ **Docker Exclusivo**: Removida execução local, foco 100% em Docker
- ✅ **Network Host**: Resolve problemas de conectividade DNS
- ✅ **Instalação Runtime**: Dependências instaladas no start para evitar problemas de build
- ✅ **Healthcheck Robusto**: Verificação de saúde aprimorada
- ✅ **Logs Detalhados**: Melhor acompanhamento do funcionamento
- ✅ **Start Script**: Instalação robusta com retry e backoff

## 📋 Configurações Avançadas

### Personalizar Modelos OpenAI
No arquivo `.env`:
```env
OPENAI_MODEL=gpt-4o-mini     # Mais rápido e barato
# ou
OPENAI_MODEL=gpt-4o          # Mais inteligente
```

### Ajustar Timeouts
Para conexões lentas, edite `docker-compose.yml`:
```yaml
healthcheck:
  interval: 120s    # Aumentar intervalo
  timeout: 60s      # Aumentar timeout
  start_period: 180s # Mais tempo para iniciar
```

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Docker Logs**: Sempre verifique `docker logs -f geratexto-bot` primeiro
- **Issues**: Use o sistema de issues do GitHub
- **Conectividade**: Teste com `docker exec geratexto-bot python3 verificar_conectividade.py`
- **Rebuild**: Quando em dúvida, use `docker-compose up --build`

## 🐛 Problemas Resolvidos (v2.4.1)

### ❌ SyntaxError: unicode error 'unicodeescape'
**Problema:** Erro de sintaxe na linha 40 do `escritor_ia.py`
```
SyntaxError: (unicode error) 'unicodeescape' codec can't decode bytes in position 2-3: truncated \UXXXXXXXX escape
```

**Solução:** Corrigido sequência de escape Unicode inválida de `\n\URL:` para `\n\nURL:`

### ✅ Status Atual
- ✅ Bot inicializando corretamente
- ✅ Todos os comandos funcionais
- ✅ Geração de posts operacional
- ✅ Processamento de URLs ativo
- ✅ Sistema de tendências funcionando

---

**GeraTexto v2.4.0** - Docker Exclusivo e Otimizado 🐳