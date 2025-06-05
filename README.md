# GeraTexto Bot 🤖

**Versão 2.3.1** - Bot Telegram inteligente para geração de conteúdo com IA

## 🚀 Recursos Principais

- **📝 Geração de Posts**: Cria conteúdo sobre qualquer tema
- **🌐 Processamento de URLs**: Extrai e resume conteúdo de páginas web
- **📈 Tendências Automáticas**: Reddit + TechCrunch + HackerNews
- **🎨 Imagens com IA**: DALL-E integrado 
- **📎 Anexos Automáticos**: Arquivos .txt para cópia fácil
- **💾 Preservação de Conteúdo**: Texto original mantido ao gerar imagens

## 🛠️ Instalação

### Método 1: Execução Local (Recomendado)

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
# ou python bot_telegram.py
```

### Método 2: Docker (Alternativo)

```bash
# Configurar variáveis
cp .env.example .env
# Edite .env com suas chaves

# Executar com Docker
docker-compose up -d

# Monitorar logs
docker logs -f geratexto-bot

# Corrigir problemas DNS (se necessário)
./fix-docker.sh
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

### Problemas Comuns:

**Erro de dependências:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Problemas de rede no Docker:**
```bash
./fix-docker.sh
```

**Bot não responde:**
- Verifique se o TELEGRAM_TOKEN está correto
- Confirme se o bot foi iniciado via @BotFather
- Teste conectividade: `python verificar_conectividade.py`

## 📁 Estrutura do Projeto

```
GeraTexto/
├── bot_telegram.py          # Bot principal
├── escritor_ia.py           # Geração de textos
├── imagem_ia.py            # Geração de imagens
├── gerador_tendencias.py   # Captação de tendências
├── run-bot.sh              # Script de execução
├── fix-docker.sh           # Correção Docker
├── posts/                  # Posts gerados
├── templates/              # Templates
└── tests/                  # Testes unitários
```

## 🧪 Testes

```bash
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
# Execução local
tail -f bot.log

# Docker
docker logs -f geratexto-bot
```

### Verificação de Status:
```bash
# Verificar conectividade
python verificar_conectividade.py

# Status dos serviços  
docker-compose ps
```

## 🔄 Atualizações Recentes (v2.3.1)

- ✅ **Correção DNS**: Resolver problemas de conectividade Docker
- ✅ **Execução Local**: Método preferencial para maior estabilidade  
- ✅ **Scripts Melhorados**: `run-bot.sh` para execução robusta
- ✅ **Configuração Simplificada**: Dependências otimizadas
- ✅ **Logs Aprimorados**: Melhor debugging e monitoramento

## 📄 Licença

MIT License - Veja [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: Use o sistema de issues do GitHub
- **Logs**: Sempre inclua logs relevantes ao reportar problemas
- **Configuração**: Confirme que todas as variáveis estão corretas

---

**GeraTexto v2.3.1** - Inteligência Artificial para Criação de Conteúdo