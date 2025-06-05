from __future__ import annotations
import os
import asyncio
import time
from pathlib import Path
import logging
import sys

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.request import HTTPXRequest
import httpx

from utils import verificar_env
from escritor_ia import gerar_post, salvar_post
from imagem_ia import gerar_imagem
from gerador_tendencias import obter_tendencias

# Configuração de logging mais detalhada
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

verificar_env()

TOKEN = os.environ["TELEGRAM_TOKEN"]
MAX_TENDENCIAS = 5


def verificar_conectividade_basica():
    """Verifica conectividade básica antes de iniciar o bot"""
    import socket
    import requests

    logger.info("🔍 Verificando conectividade...")

    # Testar resolução DNS
    try:
        socket.gethostbyname("api.telegram.org")
        logger.info("✅ DNS resolvendo corretamente")
    except socket.gaierror as e:
        logger.error(f"❌ Falha na resolução DNS: {e}")
        return False

    # Testar conectividade HTTP
    try:
        response = requests.get("https://api.telegram.org", timeout=30)
        logger.info(f"✅ Conectividade com Telegram API: {response.status_code}")
        return True
    except Exception as e:
        logger.error(f"❌ Falha na conectividade: {e}")
        return False


def criar_cliente_http_robusto():
    """Cria cliente HTTP com configurações robustas"""
    return HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=30.0,
        read_timeout=30.0,
        write_timeout=30.0,
        pool_timeout=30.0,
        http_version="1.1",
        proxy_url=None,
    )


async def inicializar_bot_com_retry(token: str, max_tentativas: int = 5):
    """Inicializa bot com sistema de retry"""
    for tentativa in range(1, max_tentativas + 1):
        try:
            logger.info(
                f"🔄 Tentativa {tentativa}/{max_tentativas} de inicialização..."
            )

            # Criar cliente HTTP robusto
            request = criar_cliente_http_robusto()

            # Construir aplicação
            app = ApplicationBuilder().token(token).request(request).build()

            # Testar conexão
            bot_info = await app.bot.get_me()
            logger.info(f"✅ Bot conectado: @{bot_info.username}")

            return app

        except Exception as e:
            logger.error(f"❌ Tentativa {tentativa} falhou: {e}")

            if tentativa < max_tentativas:
                tempo_espera = min(2**tentativa, 30)  # Backoff exponencial
                logger.info(
                    f"⏳ Aguardando {tempo_espera}s antes da próxima tentativa..."
                )
                await asyncio.sleep(tempo_espera)
            else:
                logger.error("💥 Todas as tentativas falharam!")
                raise


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /start"""
    try:
        await update.message.reply_text(
            "🤖 *GeraTexto Bot Ativo!*\n\n"
            "📝 `/gerar <tema>` - Criar post sobre um tema\n"
            "📈 `/tendencias` - Ver tendências atuais\n"
            "ℹ️ `/status` - Verificar status do bot",
            parse_mode="Markdown",
        )
    except Exception as e:
        logger.error(f"Erro no comando start: {e}")


async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /gerar"""
    try:
        if not context.args:
            await update.message.reply_text(
                "📝 Uso: `/gerar <tema>`", parse_mode="Markdown"
            )
            return

        tema = " ".join(context.args)

        # Enviar mensagem de processamento
        processing_msg = await update.message.reply_text("🔄 Gerando post...")

        try:
            post = gerar_post(tema)
            arquivo = salvar_post(tema, post)

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🎨 Adicionar imagem IA", callback_data=f"img|{arquivo}"
                    )
                ]
            ]

            await processing_msg.edit_text(
                f"✍️ **Título:** {tema}\n\n{post}",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )
        except Exception as e:
            await processing_msg.edit_text(f"❌ Erro ao gerar post: {str(e)}")

    except Exception as e:
        logger.error(f"Erro no comando gerar: {e}")


async def tendencias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /tendencias"""
    try:
        processing_msg = await update.message.reply_text("🔄 Buscando tendências...")

        try:
            topicos = obter_tendencias()[:MAX_TENDENCIAS]
            if not topicos:
                await processing_msg.edit_text(
                    "❌ Não foi possível obter tendências agora."
                )
                return

            linhas = ["📈 **Tendências Atuais:**\n"]
            for i, t in enumerate(topicos, 1):
                if t.link:
                    linhas.append(f"{i}. [{t.titulo}]({t.link})")
                else:
                    linhas.append(f"{i}. {t.titulo}")

            await processing_msg.edit_text(
                "\n".join(linhas),
                parse_mode="Markdown",
                disable_web_page_preview=True,
            )
        except Exception as e:
            await processing_msg.edit_text(f"❌ Erro ao buscar tendências: {str(e)}")

    except Exception as e:
        logger.error(f"Erro no comando tendencias: {e}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comando /status - verificar status do bot"""
    try:
        status_msg = "🤖 **Status do GeraTexto Bot**\n\n"
        status_msg += f"✅ Bot funcionando\n"
        status_msg += f"📡 Conexão ativa\n"
        status_msg += f"⏰ {time.strftime('%Y-%m-%d %H:%M:%S')}"

        await update.message.reply_text(status_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Erro no comando status: {e}")


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para callbacks de botões"""
    try:
        query = update.callback_query
        await query.answer()
        data = query.data

        if data.startswith("img|"):
            await query.message.edit_text("🎨 Gerando imagem...")

            try:
                caminho = Path(data.split("|", 1)[1])
                tema = caminho.stem
                img_path = caminho.with_suffix(".png")

                gerar_imagem(tema, img_path)

                with open(img_path, "rb") as photo:
                    await query.message.reply_photo(
                        photo, caption=f"🎨 Imagem para: {tema}"
                    )

            except Exception as e:
                await query.message.edit_text(f"❌ Erro ao gerar imagem: {str(e)}")

    except Exception as e:
        logger.error(f"Erro no callback: {e}")


async def main() -> None:
    """Função principal com inicialização robusta"""
    logger.info("🚀 Iniciando GeraTexto Bot...")

    # Verificar conectividade básica
    if not verificar_conectividade_basica():
        logger.error("💥 Falha na conectividade básica. Abortando...")
        sys.exit(1)

    try:
        # Inicializar bot com retry
        app = await inicializar_bot_com_retry(TOKEN)

        # Adicionar handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("gerar", gerar))
        app.add_handler(CommandHandler("tendencias", tendencias))
        app.add_handler(CommandHandler("status", status))
        app.add_handler(CallbackQueryHandler(callbacks))

        logger.info("🎉 Bot configurado com sucesso!")

        # Executar bot
        await app.run_polling(
            poll_interval=1.0,
            timeout=30,
            bootstrap_retries=5,
            read_timeout=30,
            write_timeout=30,
            connect_timeout=30,
            pool_timeout=30,
        )

    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")
        sys.exit(1)


def main_sync() -> None:
    """Função principal síncrona"""
    logger.info("🚀 Iniciando GeraTexto Bot...")

    # Verificar conectividade básica
    if not verificar_conectividade_basica():
        logger.error("💥 Falha na conectividade básica. Abortando...")
        sys.exit(1)

    try:
        # Construir aplicação com configurações simples
        app = ApplicationBuilder().token(TOKEN).build()

        # Adicionar handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("gerar", gerar))
        app.add_handler(CommandHandler("tendencias", tendencias))
        app.add_handler(CommandHandler("status", status))
        app.add_handler(CallbackQueryHandler(callbacks))

        logger.info("🎉 Bot configurado com sucesso!")

        # Executar bot
        app.run_polling(
            poll_interval=2.0,
            timeout=20,
        )

    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Executar função principal síncrona
    try:
        main_sync()
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"💥 Erro durante execução: {e}")
        sys.exit(1)
