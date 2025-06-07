# GeraTexto Bot 🤖

**Versão 2.5.0** – Bot do Telegram para criação de conteúdo automatizado com IA.

## Recursos
- **Geração de posts** sobre qualquer tema
- **Processamento de URLs** com resumo do conteúdo
- **Coleta de tendências** (Reddit, TechCrunch e HackerNews)
- **Imagens via DALL‑E**
- **Anexos em texto** para fácil cópia
- **Preservação do conteúdo original** ao gerar imagens

## Instalação Rápida (Docker)
1. Clone o repositório e acesse a pasta `GeraTexto`.
2. Copie `.env.example` para `.env` e adicione suas chaves API.
3. Execute `docker-compose up -d` para iniciar o bot.
4. Veja os logs com `docker logs -f geratexto-bot`.

### Obtendo as chaves
1. **Telegram**: fale com `@BotFather` e crie um bot novo.
2. **OpenAI**: gere uma chave em <https://platform.openai.com>.

## Comandos do Bot
- `/start` – inicia o bot
- `/gerar <tema ou URL>` – cria um post ou resume a URL
- `/tendencias` – mostra as tendências atuais
- `/status` – exibe o status do bot

### Exemplos
```
/gerar Inteligência Artificial em 2024
/gerar https://techcrunch.com/artigo-exemplo
/tendencias
```

## Comandos Docker úteis
### Gerenciamento
```
docker-compose up -d        # iniciar
docker-compose down         # parar
docker-compose up --build   # rebuild completo
docker logs -f geratexto-bot # acompanhar logs
```

### Manutenção e debug
```
docker exec -it geratexto-bot bash                    # shell no container
docker exec geratexto-bot python3 verificar_conectividade.py # teste de rede
docker restart geratexto-bot                          # reiniciar
```

## Troubleshooting
### Container não inicia
```
docker logs geratexto-bot
```
Se necessário, refaça o build:
```
docker-compose down
docker-compose up --build
```

### Problemas de conectividade
```
docker exec geratexto-bot python3 verificar_conectividade.py
```

## Estrutura do Projeto
```
GeraTexto/
├── docker-compose.yml      # configuração Docker
├── Dockerfile              # imagem do bot
├── start.sh                # script de inicialização
├── bot_telegram.py         # bot principal
├── escritor_ia.py          # geração de textos
├── imagem_ia.py            # geração de imagens
├── gerador_tendencias.py   # captura de tendências
├── healthcheck.py          # verificação de saúde
├── verificar_conectividade.py # teste de rede
├── posts/                  # posts gerados
├── templates/              # templates Jinja
└── tests/                  # testes unitários
```

## Executando Testes
Dentro do container:
```
docker exec geratexto-bot python -m pytest
```

## Monitoramento
```
docker logs -f geratexto-bot               # logs em tempo real
docker stats geratexto-bot                 # uso de recursos
```

## Atualização do Bot
```
docker-compose down
git pull
docker-compose up --build -d
```

## Backup e Restauração
```
docker cp geratexto-bot:/app/posts ./backup-posts-$(date +%Y%m%d)
tar -czf backup-geratexto-$(date +%Y%m%d).tar.gz posts/ templates/ .env
```
Para restaurar, copie novamente para o container e reinicie-o.

## Configurações Avançadas
Edite `.env` para escolher o modelo OpenAI e ajuste `docker-compose.yml` caso precise de timeouts maiores.

## Licença
MIT – consulte o arquivo [LICENSE](LICENSE).

## Suporte
Abra uma *issue* no GitHub ou verifique primeiro os logs com `docker logs -f geratexto-bot`.

## Histórico de Versões
### 2.5.0
- Extração automática de conteúdo ao clicar em tendência
- Posts mais ricos com base no texto da página
- Tratamento de mensagens longas
- Melhor estabilidade e prompts otimizados

### 2.4.0
- Foco total em Docker
- Instalação das dependências em tempo de execução
- Healthcheck aprimorado e logs detalhados

