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

## 🐳 Solução Docker Offline

O projeto inclui uma solução robusta para problemas de rede no Docker:

- **Dependências pré-baixadas**: Pasta `docker-deps/` com wheels Python 3.10
- **Instalação offline primeiro**: Script `start.sh` tenta instalação offline antes da online
- **Fallback automático**: Se offline falhar, tenta instalação online
- **Build simplificado**: Dockerfile sem comandos RUN que podem falhar

### Estrutura de Arquivos

```
GeraTexto/
├── docker-deps/          # Dependências offline (wheels Python 3.10)
├── start.sh             # Script de inicialização com instalação offline
├── Dockerfile           # Configuração Docker simplificada
├── run-docker.sh        # Script principal de execução
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

### Problemas de Rede Docker

Se houver problemas de conectividade:

1. **Dependências offline**: O projeto inclui todas as dependências necessárias
2. **Verificar logs**: Use `docker logs geratexto-bot` para diagnóstico
3. **Conectividade**: Verifique se o container tem acesso à internet para APIs

### Erro "ModuleNotFoundError"

Se aparecer erro de módulo não encontrado:

1. **Rebuild**: Execute `./run-docker.sh` novamente
2. **Dependências**: Verifique se a pasta `docker-deps/` existe
3. **Logs**: Verifique se a instalação offline foi bem-sucedida

## 📝 Versão Atual

**v2.1.0** - Modelo OpenAI configurável via .env + Solução Docker offline

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

## 🔧 Dependências

- python-telegram-bot==20.3
- openai==1.3.8
- requests==2.31.0
- python-dotenv==1.0.0
- pytrends==4.9.2
- jinja2==3.1.2
- Pillow==10.1.0

## 📝 Notas Técnicas

- O modelo OpenAI é configurado via `.env` e usado por todos os módulos
- Posts são salvos na pasta `posts/` com timestamp
- Imagens são geradas usando DALL-E 3
- Tendências são obtidas via Google Trends

## 📄 Licença

MIT License - veja o arquivo LICENSE para detalhes.

