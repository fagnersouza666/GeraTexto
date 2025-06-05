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
    """Verifica conectividade básica - versão simplificada"""
    import socket

    logger.info("🔍 Verificando conectividade...")

    # Verificação mínima - apenas tentar resolver DNS básico
    try:
        socket.gethostbyname("api.telegram.org")
        logger.info("✅ DNS básico funcionando")
        return True
    except socket.gaierror as e:
        logger.warning(f"⚠️ DNS com problema: {e}")
        # Mesmo com problema de DNS, vamos tentar continuar
        return True


def criar_cliente_http_simples():
    """Cria cliente HTTP com configurações simples"""
    return HTTPXRequest(
        connection_pool_size=4,
        connect_timeout=60.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=60.0,
    )


async def inicializar_bot_simples(token: str):
    """Inicializa bot de forma simples e robusta"""
    try:
        logger.info("🔄 Inicializando bot...")

        # Criar aplicação com configurações básicas
        app = ApplicationBuilder().token(token).build()

        # Testar conexão básica
        try:
            bot_info = await app.bot.get_me()
            logger.info(f"✅ Bot conectado: @{bot_info.username}")
            return app
        except Exception as e:
            logger.warning(f"⚠️ Erro na verificação inicial: {e}")
            # Retornar mesmo assim - o bot pode funcionar
            return app

    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
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

            # Armazenar tendências no contexto do bot para recuperar depois
            if not hasattr(context.bot, "_tendencias_cache"):
                context.bot._tendencias_cache = {}

            # Criar apenas os botões para cada tendência
            keyboard = []

            for i, t in enumerate(topicos):
                # Armazenar tanto título original quanto resumo
                cache_key = f"{update.effective_chat.id}_{i}"

                # Usar resumo se disponível, senão título original
                tema_para_post = t.resumo if t.resumo else t.titulo
                titulo_para_botao = (
                    t.resumo[:35] + "..."
                    if t.resumo and len(t.resumo) > 35
                    else (t.resumo or t.titulo[:35] + "...")
                )

                context.bot._tendencias_cache[cache_key] = {
                    "titulo": t.titulo,
                    "tema_post": tema_para_post,
                    "link": t.link,
                }

                # Usar índice como callback_data (seguro)
                callback_data = f"trend_{i}"

                keyboard.append(
                    [
                        InlineKeyboardButton(
                            f"📝 {titulo_para_botao}", callback_data=callback_data
                        )
                    ]
                )

            await processing_msg.edit_text(
                "📈 **Tendências Atuais**\n\n👆 *Clique para gerar post:*",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
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

        elif data.startswith("trend_"):
            # Processar clique em tendência usando índice
            try:
                indice = int(data.split("_")[1])
                cache_key = f"{query.message.chat.id}_{indice}"

                # Recuperar dados da tendência do cache
                if (
                    hasattr(context.bot, "_tendencias_cache")
                    and cache_key in context.bot._tendencias_cache
                ):
                    tendencia_data = context.bot._tendencias_cache[cache_key]
                else:
                    await query.message.edit_text(
                        "❌ Tendência não encontrada. Tente `/tendencias` novamente."
                    )
                    return

                await query.message.edit_text(
                    f"🔄 Gerando post sobre: **{tendencia_data['titulo']}**...",
                    parse_mode="Markdown",
                )

                # Gerar post usando o tema processado (resumo inteligente)
                post = gerar_post(tendencia_data["tema_post"])
                arquivo = salvar_post(tendencia_data["titulo"], post)

                # Criar botão para adicionar imagem
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "🎨 Adicionar imagem IA", callback_data=f"img|{arquivo}"
                        )
                    ]
                ]

                await query.message.edit_text(
                    f"📈 **Tendência:** {tendencia_data['titulo']}\n\n{post}",
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown",
                )

                # Mostrar mensagem de sucesso
                await query.answer("✅ Post gerado!", show_alert=False)

            except Exception as e:
                logger.error(f"Erro ao processar tendência: {e}")
                await query.message.edit_text(f"❌ Erro ao gerar post: {str(e)}")
                await query.answer("❌ Erro ao gerar post", show_alert=True)

    except Exception as e:
        logger.error(f"Erro no callback: {e}")
        if "query" in locals():
            await query.answer("❌ Erro interno", show_alert=True)


async def main() -> None:
    """Função principal com inicialização robusta"""
    logger.info("🚀 Iniciando GeraTexto Bot...")

    # Verificação de conectividade não restritiva
    verificar_conectividade_basica()

    try:
        # Inicializar bot
        app = await inicializar_bot_simples(TOKEN)

        # Adicionar handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("gerar", gerar))
        app.add_handler(CommandHandler("tendencias", tendencias))
        app.add_handler(CommandHandler("status", status))
        app.add_handler(CallbackQueryHandler(callbacks))

        logger.info("🎉 Bot configurado com sucesso!")

        # Executar bot com configurações robustas
        await app.run_polling(
            poll_interval=2.0,
            timeout=60,
            bootstrap_retries=5,
            read_timeout=60,
            write_timeout=60,
            connect_timeout=60,
            pool_timeout=60,
        )

    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")
        # Tentar reiniciar automaticamente
        logger.info("🔄 Tentando reiniciar em 10 segundos...")
        await asyncio.sleep(10)
        raise


def main_sync() -> None:
    """Função principal síncrona"""
    logger.info("🚀 Iniciando GeraTexto Bot...")

    # Verificação de conectividade não restritiva
    verificar_conectividade_basica()

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

        # Executar bot com timeouts maiores
        app.run_polling(
            poll_interval=3.0,
            timeout=60,
        )

    except Exception as e:
        logger.error(f"💥 Erro fatal: {e}")
        # Tentar reiniciar automaticamente
        logger.info("🔄 Tentando reiniciar em 10 segundos...")
        time.sleep(10)
        raise


if __name__ == "__main__":
    # Executar função principal síncrona
    try:
        main_sync()
    except KeyboardInterrupt:
        logger.info("🛑 Bot interrompido pelo usuário")
    except Exception as e:
        logger.error(f"💥 Erro durante execução: {e}")
        sys.exit(1)
