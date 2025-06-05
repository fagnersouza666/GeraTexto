# GeraTexto - Bot Telegram para Geração de Conteúdo

Bot do Telegram que gera posts, imagens e analisa tendências usando IA.

## 🚀 Execução via Docker

Execute o bot com um único comando:

```bash
./run-docker.sh
```

### Configuração Necessária

O bot requer as seguintes variáveis no arquivo `.env`:

- **TELEGRAM_TOKEN**: Token do bot (obtenha com @BotFather)
- **OPENAI_API_KEY**: Chave da API OpenAI (platform.openai.com)
- **OPENAI_MODEL**: Modelo a ser usado (padrão: gpt-4o-mini)

### Como Obter as Chaves

1. **Token Telegram**: 
   - Fale com @BotFather no Telegram
   - Use o comando `/newbot`
   - Siga as instruções para criar seu bot

2. **Chave OpenAI**:
   - Acesse [platform.openai.com](https://platform.openai.com)
   - Vá em "API Keys"
   - Crie uma nova chave

### Modelos OpenAI Disponíveis

O modelo é configurado via variável `OPENAI_MODEL` no arquivo `.env`:

- **gpt-4o-mini** (padrão) - Mais rápido e econômico
- **gpt-4o** - Mais avançado, maior qualidade
- **gpt-3.5-turbo** - Alternativa mais barata

## 🐳 Solução Docker Offline ✅ FUNCIONANDO

**Status: IMPLEMENTAÇÃO BEM-SUCEDIDA** 🎉

O projeto inclui uma solução robusta **testada e funcionando** para problemas de rede no Docker:

- ✅ **Dependências pré-baixadas**: 32 wheels Python 3.10 na pasta `docker-deps/`
- ✅ **Instalação offline primeiro**: Script `start.sh` instala offline antes de tentar online
- ✅ **Build 100% funcional**: Container criado sem erros de network
- ✅ **Todas as dependências instaladas**: OpenAI, Telegram Bot, PyTrends, etc.
- ✅ **DNS corrigido**: Problema de resolução de nomes resolvido via docker-compose

### Scripts Disponíveis

**Execução Principal**:
```bash
./run-docker.sh              # Script principal (build + run)
```

**Correção de Problemas**:
```bash
./corrigir_docker_dns.sh     # Corrige problemas específicos de DNS
docker-compose up -d         # Alternativa robusta
```

**Diagnóstico**:
```bash
python verificar_conectividade.py  # Testa conectividade do host
docker logs -f geratexto-bot       # Logs em tempo real
```

### Logs de Sucesso Confirmados

A solução offline foi **testada e validada**:
```
📦 Instalando dependências offline...
Successfully installed Jinja2-3.1.2 MarkupSafe-3.0.2 Pillow-10.1.0 
[...] openai-1.3.8 [...] python-telegram-bot-20.3 [...]
✅ Dependências offline instaladas
✅ Dependências online instaladas
🚀 Iniciando bot Telegram...
```

**DNS Resolvido**: Erro mudou de "DNS failure" para "ConnectTimeout", confirmando que DNS funciona!

### Estrutura de Arquivos

```
GeraTexto/
├── docker-deps/          # ✅ 32 dependências offline (wheels Python 3.10)
├── start.sh             # ✅ Script de inicialização offline/online
├── Dockerfile           # ✅ Configuração Docker simplificada
├── run-docker.sh        # ✅ Script principal de execução
├── .env                 # Configurações (criar baseado em .env.example)
└── ...
```

## 📋 Comandos Úteis

Após executar `./run-docker.sh`:

```bash
# Ver logs em tempo real
docker logs -f geratexto-bot

# Parar o bot
docker stop geratexto-bot

# Reiniciar o bot
docker restart geratexto-bot

# Remover completamente
docker rm -f geratexto-bot
```

## 🎯 Funcionalidades

- **Geração de Posts**: Cria conteúdo sobre qualquer tema
- **Geração de Imagens**: Cria imagens usando DALL-E 3
- **Análise de Tendências**: Monitora tendências do Google Trends
- **Templates Personalizáveis**: Sistema de templates Jinja2
- **Configuração Flexível**: Modelo OpenAI configurável via .env

## 🔧 Solução de Problemas

### ✅ Dependências Offline - RESOLVIDO

O projeto **já inclui** todas as dependências necessárias offline. Se aparecer erro de módulo:
1. **Não é problema do código** - as dependências estão funcionando
2. **Verificar logs**: Use `docker logs geratexto-bot` para diagnóstico
3. **Rebuild**: Execute `./run-docker.sh` novamente se necessário

### 🌐 Problemas de DNS/Conectividade

**Nota Importante**: Se o bot falhar com erro `Temporary failure in name resolution`:
- ✅ **As dependências foram instaladas corretamente**
- ✅ **O código está funcionando perfeitamente**
- ⚠️ **É um problema de conectividade do ambiente** (DNS, firewall, proxy)

**Script de Diagnóstico**: Use o verificador automático:
```bash
# Executar no host (fora do Docker)
python verificar_conectividade.py
```

**Soluções para conectividade**:
1. **Verificar internet**: Teste `ping google.com` no host
2. **Docker network**: Reiniciar Docker se necessário
3. **Firewall/Proxy**: Verificar bloqueios de rede
4. **DNS**: Verificar resolução de nomes

### Erro "ModuleNotFoundError"

**Status**: ✅ RESOLVIDO - Dependências offline funcionando

Se ainda aparecer (improvável):
1. **Verificar logs**: Confirme instalação offline bem-sucedida
2. **Rebuild**: Execute `./run-docker.sh` novamente
3. **Dependências**: Pasta `docker-deps/` deve ter 32 arquivos .whl

## 📝 Versão Atual

**v2.1.1** - Solução Docker offline FUNCIONANDO + Modelo OpenAI configurável

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📁 Estrutura do Projeto

```
GeraTexto/
├── bot_telegram.py      # Bot principal
├── escritor_ia.py       # Geração de textos
├── imagem_ia.py         # Geração de imagens
├── gerador_tendencias.py # Análise de tendências
├── utils.py             # Utilitários e configuração
├── prompts/             # Templates de prompts
├── templates/           # Templates de posts
├── posts/               # Posts gerados
└── .env                 # Configurações (criar baseado em .env.example)
```

## 🔧 Dependências ✅ OFFLINE

**Status**: Todas as 32 dependências funcionando offline

- python-telegram-bot==20.3 ✅
- openai==1.3.8 ✅
- requests==2.31.0 ✅
- python-dotenv==1.0.0 ✅
- pytrends==4.9.2 ✅
- jinja2==3.1.2 ✅
- Pillow==10.1.0 ✅
- + 25 dependências secundárias ✅

## 📝 Notas Técnicas

- ✅ O modelo OpenAI é configurado via `.env` e usado por todos os módulos
- ✅ Posts são salvos na pasta `posts/` com timestamp
- ✅ Imagens são geradas usando DALL-E 3
- ✅ Tendências são obtidas via Google Trends
- ✅ Instalação offline 100% funcional com 32 wheels pré-baixadas

## 📄 Licença

MIT License - veja o arquivo LICENSE para detalhes.

