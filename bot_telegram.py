from __future__ import annotations
import os
from pathlib import Path

import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from utils import verificar_env

from escritor_ia import gerar_post, salvar_post
from imagem_ia import gerar_imagem
from gerador_tendencias import obter_tendencias

logging.basicConfig(level=logging.INFO)

verificar_env()

TOKEN = os.environ["TELEGRAM_TOKEN"]
MAX_TENDENCIAS = 5


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Envie /gerar <tema> para criar um post.")


async def gerar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Uso: /gerar <tema>")
        return
    tema = " ".join(context.args)
    post = gerar_post(tema)
    arquivo = salvar_post(tema, post)
    keyboard = [
        [InlineKeyboardButton("Adicionar imagem IA", callback_data=f"img|{arquivo}")]
    ]
    await update.message.reply_text(
        f"\u270d\ufe0f Título: {tema}\n\n{post}",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown",
    )


async def tendencias(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    topicos = obter_tendencias()[:MAX_TENDENCIAS]
    if not topicos:
        await update.message.reply_text("N\u00e3o foi poss\u00edvel obter tend\u00eancias agora.")
        return
    linhas = []
    for t in topicos:
        if t.link:
            linhas.append(f"- [{t.titulo}]({t.link})")
        else:
            linhas.append(f"- {t.titulo}")
    await update.message.reply_text(
        "\n".join(linhas),
        parse_mode="Markdown",
        disable_web_page_preview=True,
    )


async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data
    if data.startswith("img|"):
        caminho = Path(data.split("|", 1)[1])
        tema = caminho.stem
        img_path = caminho.with_suffix(".png")
        gerar_imagem(tema, img_path)
        await query.message.reply_photo(img_path.open("rb"))


def main() -> None:
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gerar", gerar))
    app.add_handler(CommandHandler("tendencias", tendencias))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.run_polling()


if __name__ == "__main__":
    main()

