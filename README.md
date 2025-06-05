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

- `gpt-4o-mini` (padrão - mais econômico)
- `gpt-4o` (mais avançado)
- `gpt-3.5-turbo` (alternativa econômica)

## 📋 Comandos do Bot

- `/start` - Inicializar o bot
- `/gerar <tema>` - Gerar post sobre um tema
- `/tendencias` - Ver tendências atuais
- `/imagem <descrição>` - Gerar imagem

## 🛠️ Comandos Docker Úteis

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

## 🐛 Solução de Problemas

### Erro de Rede no Docker
Se houver problemas de rede durante o build Docker, o script tentará usar docker-compose como fallback.

### Dependências Não Encontradas
Certifique-se de que o arquivo `.env` está configurado corretamente com todas as variáveis necessárias.

## 📄 Licença

MIT License - veja o arquivo LICENSE para detalhes.

