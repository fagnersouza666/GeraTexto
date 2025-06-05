# GeraTexto Bot 🤖

**Versão 2.3.1** - Bot Telegram inteligente para geração de conteúdo com IA

## 🚀 Recursos Principais

- **📝 Geração de Posts**: Cria conteúdo sobre qualquer tema
- **🌐 Processamento de URLs**: Extrai e resume conteúdo de páginas web
- **📈 Tendências Automáticas**: Reddit + TechCrunch + HackerNews
- **🎨 Imagens com IA**: DALL-E integrado 
- **📎 Anexos Automáticos**: Arquivos .txt para cópia fácil
- **💾 Preservação de Conteúdo**: Texto original mantido ao gerar imagens

## 🛠️ Instalação e Execução

### ⭐ Método Principal: Execução Local

**Este é o método recomendado e mais estável:**

```bash
# 1. Clonar repositório
git clone <repository-url>
cd GeraTexto

# 2. Criar ambiente virtual
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate no Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar variáveis de ambiente
cp .env.example .env
# Edite .env com suas chaves API

# 5. Executar bot
./run-bot.sh
```

### 🐳 Método Alternativo: Docker

**⚠️ Limitações conhecidas: problemas de rede em alguns sistemas**

```bash
# Configurar variáveis
cp .env.example .env
# Edite .env com suas chaves

# Tentar Docker (pode falhar por problemas de rede)
docker-compose up -d

# Se houver problemas de rede:
./fix-docker.sh

# Para verificar logs:
docker logs -f geratexto-bot
```

## ⚙️ Configuração

Crie o arquivo `.env` com:

```env
TELEGRAM_TOKEN=seu_token_telegram
OPENAI_API_KEY=sua_chave_openai
OPENAI_MODEL=gpt-4o-mini
```

### Como Obter as Chaves:

1. **Telegram Token**: @BotFather no Telegram
2. **OpenAI API Key**: [platform.openai.com](https://platform.openai.com)

## 📋 Comandos do Bot

- `/start` - Inicializar bot
- `/gerar <tema>` - Criar post sobre tema
- `/gerar <URL>` - Extrair e criar post de URL
- `/tendencias` - Ver tendências atuais  
- `/status` - Verificar status do bot

## 💡 Exemplos de Uso

```
/gerar Inteligência Artificial
/gerar https://techcrunch.com/artigo-exemplo
/tendencias
```

## 🔧 Troubleshooting

### ✅ Execução Local (Recomendado)

**Se o bot não iniciar:**
```bash
# Verificar ambiente virtual
source .venv/bin/activate

# Reinstalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Verificar variáveis de ambiente
cat .env

# Executar com logs detalhados
python bot_telegram.py
```

### 🐳 Problemas no Docker

**Erro "network bridge not found":**
- Este é um problema conhecido em alguns sistemas
- **Solução**: Use execução local com `./run-bot.sh`

**Erro "ModuleNotFoundError":**
```bash
# Limpar e reconstruir
./fix-docker.sh
```

**Problemas de DNS:**
```bash
# Script de correção
./fix-docker.sh
```

### 🚨 Problemas Gerais

**Bot não responde no Telegram:**
- Verifique se o TELEGRAM_TOKEN está correto
- Confirme se o bot foi iniciado via @BotFather
- Teste conectividade: `python verificar_conectividade.py`

**Erro de API OpenAI:**
- Verifique se OPENAI_API_KEY está correta
- Confirme se há créditos na conta OpenAI

## 📁 Estrutura do Projeto

```
GeraTexto/
├── bot_telegram.py          # Bot principal
├── escritor_ia.py           # Geração de textos
├── imagem_ia.py            # Geração de imagens
├── gerador_tendencias.py   # Captação de tendências
├── run-bot.sh              # ⭐ Script de execução principal
├── fix-docker.sh           # Correção Docker
├── posts/                  # Posts gerados
├── templates/              # Templates
└── tests/                  # Testes unitários
```

## 🧪 Testes

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Executar todos os testes
python -m pytest

# Teste específico
python -m pytest tests/test_escritor.py -v

# Com coverage
python -m pytest --cov=. tests/
```

## 📊 Monitoramento

### Logs em Tempo Real:
```bash
# Execução local (recomendado)
# Os logs aparecem diretamente no terminal

# Docker (se funcionando)
docker logs -f geratexto-bot
```

### Verificação de Status:
```bash
# Verificar se está executando
ps aux | grep bot_telegram

# Verificar conectividade
python verificar_conectividade.py

# Status Docker (se usando)
docker-compose ps
```

## 🎯 Recomendações de Uso

1. **🥇 Primeira Opção**: `./run-bot.sh` (execução local)
2. **🥈 Segunda Opção**: `docker-compose up -d` (Docker)
3. **🔧 Se Docker falhar**: Use sempre execução local

## 🔄 Atualizações Recentes (v2.3.1)

- ✅ **Execução Local Otimizada**: Método principal e mais estável
- ✅ **Script run-bot.sh**: Execução simplificada e robusta
- ✅ **Correção DNS Docker**: Melhorias para ambientes que suportam
- ⚠️ **Docker Limitado**: Problemas de rede em alguns sistemas
- ✅ **Logs Aprimorados**: Melhor debugging e monitoramento

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Método Recomendado**: Sempre tente `./run-bot.sh` primeiro
- **Issues**: Use o sistema de issues do GitHub
- **Logs**: Sempre inclua logs relevantes ao reportar problemas
- **Docker**: Se houver problemas, mude para execução local

---

**GeraTexto v2.3.1** - Execução Local Otimizada 🎯