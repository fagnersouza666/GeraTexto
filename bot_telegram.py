from __future__ import annotations
import os
from pathlib import Path
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

from utils import verificar_env

from escritor_ia import gerar_post, salvar_post
from imagem_ia import gerar_imagem

verificar_env()
TOKEN = os.getenv("TELEGRAM_TOKEN")


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
    app.add_handler(CallbackQueryHandler(callbacks))
    app.run_polling()


if __name__ == "__main__":
    main()

