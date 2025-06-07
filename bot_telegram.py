from __future__ import annotations
import os
import asyncio
import time
from pathlib import Path
import logging
import sys
from datetime import datetime

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
from escritor_ia import (
    gerar_post,
    salvar_post,
    salvar_texto_puro,
    eh_url_valida,
    gerar_post_de_url,
)
from imagem_ia import gerar_imagem
from gerador_tendencias import obter_tendencias
from tradutor import traduzir_para_pt

# Configuração de logging mais detalhada
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

verificar_env()

TOKEN = os.environ["TELEGRAM_TOKEN"]
MAX_TENDENCIAS = 5


def verificar_conectividade_basica():
    """Verifica conectividade básica - versão melhorada"""
    import socket
    import subprocess

    logger.info("🔍 Verificando conectividade...")

    # Tentar resolver múltiplos serviços DNS
    hosts_teste = ["8.8.8.8", "api.telegram.org", "api.openai.com", "google.com"]

    conexoes_ok = 0
    for host in hosts_teste:
        try:
            if host in ["8.8.8.8"]:
                # Teste direto de conectividade
                sock = socket.create_connection((host, 53), timeout=5)
                sock.close()
            else:
                # Teste de resolução DNS
                socket.gethostbyname(host)

            logger.info(f"✅ {host} - OK")
            conexoes_ok += 1
        except Exception as e:
            logger.warning(f"⚠️ {host} - Falha: {e}")

    if conexoes_ok > 0:
        logger.info("✅ Conectividade básica funcionando")
    else:
        logger.warning("⚠️ Problemas de conectividade detectados")
        # Tentar limpar cache DNS
        try:
            subprocess.run(
                ["systemctl", "restart", "systemd-resolved"],
                capture_output=True,
                timeout=10,
            )
        except:
            pass

    return True  # Sempre retorna True para tentar continuar


def criar_cliente_http_robusta():
    """Cria cliente HTTP com configurações robustas para Docker"""
    return HTTPXRequest(
        connection_pool_size=8,
        connect_timeout=30.0,
        read_timeout=60.0,
        write_timeout=60.0,
        pool_timeout=30.0,
    )


async def inicializar_bot_robusta(token: str, max_tentativas=5):
    """Inicializa bot de forma robusta com retry automático"""
    for tentativa in range(1, max_tentativas + 1):
        try:
            logger.info(
                f"🔄 Tentativa {tentativa}/{max_tentativas} - Inicializando bot..."
            )

            # Criar aplicação com configurações robustas
            request = criar_cliente_http_robusta()
            app = ApplicationBuilder().token(token).request(request).build()

            # Testar conexão com retry
            try:
                bot_info = await app.bot.get_me()
                logger.info(f"✅ Bot conectado: @{bot_info.username}")
                return app
            except Exception as e:
                logger.warning(f"⚠️ Erro na verificação (tentativa {tentativa}): {e}")

                if tentativa < max_tentativas:
                    wait_time = min(tentativa * 5, 30)  # Backoff exponencial limitado
                    logger.info(
                        f"⏳ Aguardando {wait_time}s antes da próxima tentativa..."
                    )
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    logger.warning("⚠️ Máximo de tentativas atingido, prosseguindo...")
                    return app

        except Exception as e:
            logger.error(f"❌ Erro na inicialização (tentativa {tentativa}): {e}")

            if tentativa < max_tentativas:
                wait_time = min(tentativa * 10, 60)
                logger.info(f"⏳ Aguardando {wait_time}s antes da próxima tentativa...")
                await asyncio.sleep(wait_time)
            else:
                logger.error("❌ Falha na inicialização após todas as tentativas")
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
                "�� Uso: `/gerar <tema ou URL>`\n\n"
                "💡 **Exemplos:**\n"
                "• `/gerar Inteligência Artificial`\n"
                "• `/gerar https://example.com/artigo`",
                parse_mode="Markdown",
            )
            return

        input_usuario = " ".join(context.args)

        # Enviar mensagem de processamento
        processing_msg = await update.message.reply_text("🔄 Gerando post...")

        try:
            # Verificar se é uma URL
            if eh_url_valida(input_usuario):
                # Processar URL
                await processing_msg.edit_text("🌐 Extraindo conteúdo da URL...")

                try:
                    titulo, post = gerar_post_de_url(input_usuario)
                    await processing_msg.edit_text(
                        "📝 Gerando post baseado no conteúdo extraído..."
                    )

                except Exception as e:
                    await processing_msg.edit_text(
                        f"❌ Erro ao processar URL: {str(e)}"
                    )
                    return
            else:
                # Processar como tema normal
                tema = input_usuario
                titulo = tema
                post = gerar_post(tema)

            # Salvar arquivos
            arquivo = salvar_post(titulo, post)
            arquivo_txt = salvar_texto_puro(titulo, post)

            # Criar botão para adicionar imagem com callback_data seguro
            callback_img = f"img|{arquivo}"

            # Verificar se callback_data não excede 64 bytes
            if len(callback_img.encode()) > 64:
                # Usar apenas o nome do arquivo sem path se for muito longo
                nome_arquivo = arquivo.name
                callback_img = f"img|{nome_arquivo}"

                # Se ainda for muito longo, usar apenas timestamp
                if len(callback_img.encode()) > 64:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    callback_img = f"img|{timestamp}"

            keyboard = [
                [
                    InlineKeyboardButton(
                        "🎨 Adicionar imagem IA", callback_data=callback_img
                    )
                ]
            ]

            # Mostrar origem se foi de URL
            origem_texto = (
                f"\n🌐 {input_usuario}" if eh_url_valida(input_usuario) else ""
            )

            # Validar tamanho da mensagem (limite Telegram: 4096 caracteres)
            mensagem_completa = f"✍️ {titulo}{origem_texto}\n\n{post}"

            if len(mensagem_completa) > 4000:  # Margem de segurança
                # Truncar o post mantendo o título e origem
                cabecalho = f"✍️ {titulo}{origem_texto}\n\n"
                espaco_disponivel = 4000 - len(cabecalho) - 50  # Margem para "..."

                post_truncado = (
                    post[:espaco_disponivel]
                    + "\n\n✂️ *Post truncado. Veja arquivo anexo para versão completa.*"
                )
                mensagem_completa = cabecalho + post_truncado

            await processing_msg.edit_text(
                mensagem_completa,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="Markdown",
            )

            # Enviar arquivo .txt como anexo/documento
            with open(arquivo_txt, "rb") as document:
                await processing_msg.reply_document(
                    document,
                    caption=f"📝 **Texto limpo para cópia**\n\n🔗 Arquivo: `{arquivo_txt.name}`\n💡 *Clique para baixar ou visualizar*",
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

            msg_linhas = ["📈 **Tendências Atuais**", ""]

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

                try:
                    traducao = traduzir_para_pt(t.titulo)
                except Exception:
                    traducao = t.titulo
                msg_linhas.append(f"{i+1}. {t.titulo} - {traducao}")

            msg_linhas.append("")
            msg_linhas.append("👆 *Clique para gerar post:*")

            await processing_msg.edit_text(
                "\n".join(msg_linhas),
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
            # Editar apenas para mostrar que está gerando
            await query.message.edit_reply_markup(reply_markup=None)

            # Enviar mensagem temporária de processamento
            processing_msg = await query.message.reply_text("🎨 Gerando imagem...")

            try:
                arquivo_info = data.split("|", 1)[1]

                # Se é só um nome de arquivo, procurar na pasta posts
                if not "/" in arquivo_info:
                    # Procurar arquivo na pasta posts
                    posts_dir = Path("posts")
                    arquivos_encontrados = list(posts_dir.glob(f"*{arquivo_info}*"))

                    if arquivos_encontrados:
                        caminho = arquivos_encontrados[0]  # Pegar o primeiro encontrado
                    else:
                        # Se não encontrou, tentar usar como timestamp
                        arquivos_recentes = sorted(
                            posts_dir.glob("*.md"),
                            key=lambda x: x.stat().st_mtime,
                            reverse=True,
                        )
                        if arquivos_recentes:
                            caminho = arquivos_recentes[0]  # Pegar o mais recente
                        else:
                            raise FileNotFoundError("Nenhum arquivo encontrado")
                else:
                    caminho = Path(arquivo_info)

                tema = (
                    caminho.stem.split("_", 2)[-1]
                    if "_" in caminho.stem
                    else caminho.stem
                )
                img_path = caminho.with_suffix(".png")

                # Gerar imagem
                gerar_imagem(tema, img_path)

                # Salvar texto puro em arquivo .txt para fácil cópia
                conteudo_post = caminho.read_text(encoding="utf-8")
                arquivo_txt = salvar_texto_puro(tema, conteudo_post)

                # Deletar mensagem de processamento
                await processing_msg.delete()

                # Enviar imagem com caption informativo (sem substituir o texto original)
                with open(img_path, "rb") as photo:
                    await query.message.reply_photo(
                        photo,
                        caption=f"🎨 **Imagem para:** {tema}\n\n📄 *Arquivo de texto enviado em anexo abaixo*",
                        parse_mode="Markdown",
                    )

                # Enviar arquivo .txt como anexo/documento
                with open(arquivo_txt, "rb") as document:
                    await query.message.reply_document(
                        document,
                        caption=f"📝 **Texto limpo para cópia**\n\n🔗 Arquivo: `{arquivo_txt.name}`\n💡 *Clique para baixar ou visualizar*",
                        parse_mode="Markdown",
                    )

            except Exception as e:
                await processing_msg.edit_text(f"❌ Erro ao gerar imagem: {str(e)}")

                # Restaurar botão se houve erro
                keyboard = [
                    [InlineKeyboardButton("🎨 Adicionar imagem IA", callback_data=data)]
                ]
                await query.message.edit_reply_markup(
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )

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

                # Se tem link da notícia, processar como URL (extrair conteúdo)
                if tendencia_data.get("link"):
                    await query.message.edit_text(
                        f"🌐 Extraindo conteúdo de: **{tendencia_data['titulo']}**...",
                        parse_mode="Markdown",
                    )

                    try:
                        # Processar URL como se fosse comando /gerar <URL>
                        titulo, post = gerar_post_de_url(tendencia_data["link"])
                        arquivo = salvar_post(titulo, post)
                    except Exception as e:
                        # Fallback: usar o método antigo se falhar
                        await query.message.edit_text(
                            f"⚠️ Erro ao extrair conteúdo, usando título: **{tendencia_data['titulo']}**...",
                            parse_mode="Markdown",
                        )
                        titulo = tendencia_data["titulo"]
                        post = gerar_post(tendencia_data["tema_post"])
                        arquivo = salvar_post(titulo, post)
                else:
                    # Fallback: se não tem link, usar o método antigo
                    titulo = tendencia_data["titulo"]
                    post = gerar_post(tendencia_data["tema_post"])
                    arquivo = salvar_post(titulo, post)

                # Salvar também arquivo .txt para anexar
                arquivo_txt = salvar_texto_puro(titulo, post)

                # Criar botão para adicionar imagem com callback_data seguro
                callback_img = f"img|{arquivo}"

                # Verificar se callback_data não excede 64 bytes
                if len(callback_img.encode()) > 64:
                    # Usar apenas o nome do arquivo sem path se for muito longo
                    nome_arquivo = arquivo.name
                    callback_img = f"img|{nome_arquivo}"

                    # Se ainda for muito longo, usar apenas timestamp
                    if len(callback_img.encode()) > 64:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        callback_img = f"img|{timestamp}"

                keyboard = [
                    [
                        InlineKeyboardButton(
                            "🎨 Adicionar imagem IA", callback_data=callback_img
                        )
                    ]
                ]

                # Mostrar origem se foi processado via URL
                origem_texto = (
                    f"\n🌐 {tendencia_data['link']}"
                    if tendencia_data.get("link")
                    else ""
                )

                # Validar tamanho da mensagem (limite Telegram: 4096 caracteres)
                mensagem_completa = f"📈 **{titulo}**{origem_texto}\n\n{post}"

                if len(mensagem_completa) > 4000:  # Margem de segurança
                    # Truncar o post mantendo o título e origem
                    cabecalho = f"📈 **{titulo}**{origem_texto}\n\n"
                    espaco_disponivel = 4000 - len(cabecalho) - 50  # Margem para "..."

                    post_truncado = (
                        post[:espaco_disponivel]
                        + "\n\n✂️ *Post truncado. Veja arquivo anexo para versão completa.*"
                    )
                    mensagem_completa = cabecalho + post_truncado

                await query.message.edit_text(
                    mensagem_completa,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown",
                )

                # Enviar arquivo .txt como anexo/documento
                with open(arquivo_txt, "rb") as document:
                    await query.message.reply_document(
                        document,
                        caption=f"📝 **Texto limpo para cópia**\n\n🔗 Arquivo: `{arquivo_txt.name}`\n💡 *Clique para baixar ou visualizar*",
                        parse_mode="Markdown",
                    )

                # Mostrar mensagem de sucesso
                await query.answer("✅ Post gerado!", show_alert=False)

            except Exception as e:
                logger.error(f"Erro ao processar tendência: {e}")
                try:
                    await query.message.edit_text(f"❌ Erro ao gerar post: {str(e)}")
                except:
                    # Se falhar ao editar, enviar nova mensagem
                    await query.message.reply_text(f"❌ Erro ao gerar post: {str(e)}")

                try:
                    await query.answer("❌ Erro ao gerar post", show_alert=True)
                except:
                    pass  # Ignorar se não conseguir responder o callback

    except Exception as e:
        logger.error(f"Erro no callback: {e}")
        try:
            if "query" in locals():
                await query.answer("❌ Erro interno", show_alert=True)
        except:
            pass  # Ignorar se não conseguir responder


async def main() -> None:
    """Função principal com inicialização robusta"""
    logger.info("🚀 Iniciando GeraTexto Bot...")

    # Verificação de conectividade não restritiva
    verificar_conectividade_basica()

    try:
        # Inicializar bot
        app = await inicializar_bot_robusta(TOKEN)

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
    """Função principal síncrona com configurações robustas"""
    max_tentativas = 3

    for tentativa in range(1, max_tentativas + 1):
        try:
            logger.info(
                f"🚀 Iniciando GeraTexto Bot (tentativa {tentativa}/{max_tentativas})..."
            )

            # Verificação de conectividade
            verificar_conectividade_basica()

            # Construir aplicação com configurações robustas
            request = criar_cliente_http_robusta()
            app = ApplicationBuilder().token(TOKEN).request(request).build()

            # Adicionar handlers
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("gerar", gerar))
            app.add_handler(CommandHandler("tendencias", tendencias))
            app.add_handler(CommandHandler("status", status))
            app.add_handler(CallbackQueryHandler(callbacks))

            logger.info("🎉 Bot configurado com sucesso!")

            # Executar bot com timeouts maiores e configurações robustas
            app.run_polling(
                poll_interval=3.0,
                timeout=30,
                bootstrap_retries=5,
                read_timeout=60,
                write_timeout=60,
                connect_timeout=30,
                pool_timeout=30,
            )

            # Se chegou aqui, foi interrompido normalmente
            break

        except Exception as e:
            logger.error(f"💥 Erro fatal na tentativa {tentativa}: {e}")

            if tentativa < max_tentativas:
                wait_time = tentativa * 15  # 15s, 30s para próximas tentativas
                logger.info(f"🔄 Tentando reiniciar em {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                logger.error("❌ Todas as tentativas falharam!")
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
