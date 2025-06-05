#!/usr/bin/env python3
"""
Healthcheck para GeraTexto Bot
Verifica se o bot está funcionando corretamente
"""

import sys
import socket
import requests
import os
from telegram import Bot
import asyncio
import logging

# Configurar logging
logging.basicConfig(level=logging.WARNING)  # Reduzir ruído nos logs


async def verificar_bot():
    """Verifica se o bot está respondendo"""
    try:
        token = os.environ.get("TELEGRAM_TOKEN")
        if not token:
            return False, "Token não encontrado"

        bot = Bot(token=token)

        # Timeout mais baixo para healthcheck
        bot_info = await bot.get_me()

        return True, f"Bot OK: @{bot_info.username}"

    except Exception as e:
        return False, f"Bot falhou: {e}"


def verificar_dns():
    """Verifica resolução DNS"""
    try:
        socket.gethostbyname("api.telegram.org")
        return True, "DNS OK"
    except Exception as e:
        return False, f"DNS falhou: {e}"


def verificar_conectividade():
    """Verifica conectividade básica"""
    try:
        response = requests.get("https://api.telegram.org", timeout=10)
        return True, f"HTTP OK: {response.status_code}"
    except Exception as e:
        return False, f"HTTP falhou: {e}"


async def main():
    """Executa todos os checks"""
    checks = [
        ("DNS", verificar_dns),
        ("HTTP", verificar_conectividade),
        ("Bot", verificar_bot),
    ]

    todos_ok = True

    for nome, func in checks:
        try:
            if asyncio.iscoroutinefunction(func):
                sucesso, msg = await func()
            else:
                sucesso, msg = func()

            if not sucesso:
                print(f"❌ {nome}: {msg}")
                todos_ok = False
            else:
                print(f"✅ {nome}: {msg}")

        except Exception as e:
            print(f"❌ {nome}: Erro - {e}")
            todos_ok = False

    if todos_ok:
        print("🎉 Healthcheck PASSOU - Bot funcionando!")
        sys.exit(0)
    else:
        print("💥 Healthcheck FALHOU - Bot com problemas!")
        sys.exit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"💥 Erro no healthcheck: {e}")
        sys.exit(1)
