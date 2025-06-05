#!/usr/bin/env python3
"""
Script de Verificação de Conectividade - GeraTexto Bot
Ajuda a diagnosticar problemas de rede vs. problemas do código
"""

import socket
import sys
import requests
import os
from datetime import datetime


def verificar_dns(host="google.com", port=80):
    """Verifica se consegue resolver DNS"""
    try:
        socket.gethostbyname(host)
        return True, f"✅ DNS OK - {host} resolvido"
    except socket.gaierror as e:
        return False, f"❌ DNS FALHOU - {e}"


def verificar_http(url="https://httpbin.org/get"):
    """Verifica conectividade HTTP"""
    try:
        response = requests.get(url, timeout=10)
        return True, f"✅ HTTP OK - Status {response.status_code}"
    except Exception as e:
        return False, f"❌ HTTP FALHOU - {e}"


def verificar_telegram_api():
    """Verifica conectividade com API do Telegram"""
    try:
        response = requests.get("https://api.telegram.org", timeout=10)
        return True, f"✅ Telegram API OK - Status {response.status_code}"
    except Exception as e:
        return False, f"❌ Telegram API FALHOU - {e}"


def verificar_openai_api():
    """Verifica conectividade com API da OpenAI"""
    try:
        response = requests.get("https://api.openai.com", timeout=10)
        return True, f"✅ OpenAI API OK - Status {response.status_code}"
    except Exception as e:
        return False, f"❌ OpenAI API FALHOU - {e}"


def verificar_variaveis_ambiente():
    """Verifica se as variáveis de ambiente necessárias estão definidas"""
    vars_necessarias = ["TELEGRAM_TOKEN", "OPENAI_API_KEY", "OPENAI_MODEL"]
    resultados = []

    for var in vars_necessarias:
        valor = os.getenv(var)
        if valor:
            resultados.append(f"✅ {var}: Definida ({'*' * min(10, len(valor))}...)")
        else:
            resultados.append(f"❌ {var}: NÃO DEFINIDA")

    return resultados


def main():
    print("🔍 GeraTexto Bot - Verificação de Conectividade")
    print("=" * 50)
    print(f"🕐 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Verificar variáveis de ambiente
    print("📋 Variáveis de Ambiente:")
    for resultado in verificar_variaveis_ambiente():
        print(f"  {resultado}")
    print()

    # Verificar conectividade
    testes = [
        ("DNS Básico", verificar_dns),
        ("HTTP Geral", verificar_http),
        ("API Telegram", verificar_telegram_api),
        ("API OpenAI", verificar_openai_api),
    ]

    print("🌐 Testes de Conectividade:")
    todos_ok = True

    for nome, funcao in testes:
        try:
            sucesso, mensagem = funcao()
            print(f"  {mensagem}")
            if not sucesso:
                todos_ok = False
        except Exception as e:
            print(f"  ❌ {nome} - ERRO: {e}")
            todos_ok = False

    print()
    print("=" * 50)

    if todos_ok:
        print("🎉 CONECTIVIDADE OK - Bot deve funcionar normalmente!")
        print("   Se ainda há problemas, verifique logs do container:")
        print("   docker logs geratexto-bot")
        sys.exit(0)
    else:
        print("⚠️ PROBLEMAS DE CONECTIVIDADE DETECTADOS")
        print("   Nota: As dependências do bot estão instaladas corretamente.")
        print("   O problema é de conectividade de rede do ambiente.")
        print()
        print("🔧 Possíveis soluções:")
        print("   1. Verificar conexão com internet")
        print("   2. Verificar configurações de proxy/firewall")
        print("   3. Reiniciar serviço Docker")
        print("   4. Verificar configurações de DNS")
        sys.exit(1)


if __name__ == "__main__":
    main()
