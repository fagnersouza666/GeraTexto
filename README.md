# GeraTexto

Bot de Telegram para gerar conteúdos sobre inteligência artificial e tecnologia. O objetivo é criar posts prontos para LinkedIn a partir de temas em alta, opcionalmente com imagem gerada por IA.

## Instalação

1. Crie um ambiente virtual (opcional):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Crie um arquivo `.env` com as seguintes variáveis:
   ```
   TELEGRAM_TOKEN=seu_token
   OPENAI_API_KEY=sua_chave
   ```

## Uso

Execute o bot com:
```bash
python bot_telegram.py
```

No Telegram, envie `/gerar <tema>` para receber o conteúdo gerado. O texto será salvo em `conteudos_gerados/`.

## Docker

Voce tambem pode executar tudo em um container Docker. Construa a imagem:

```bash
docker build -t geratexto .
```

Depois rode o container passando as variaveis de ambiente:

```bash
docker run --env TELEGRAM_TOKEN=seu_token --env OPENAI_API_KEY=sua_chave geratexto
```
