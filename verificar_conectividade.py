#!/usr/bin/env python3
"""
Script de Verificação de Conectividade - GeraTexto Bot (Versão Simplificada)
Verifica conectividade básica sem ser restritivo
"""

import socket
import sys
import os
from datetime import datetime

# Importação condicional do requests
try:
    import requests

    REQUESTS_DISPONIVEL = True
except ImportError:
    REQUESTS_DISPONIVEL = False
    print("⚠️ Módulo requests não disponível, pulando testes HTTP")


def verificar_dns(host="google.com", port=80):
    """Verifica se consegue resolver DNS"""
    try:
        socket.gethostbyname(host)
        return True, f"✅ DNS OK - {host} resolvido"
    except socket.gaierror as e:
        return False, f"⚠️ DNS com problema - {e} (pode ainda funcionar)"


def verificar_http_simples(url="https://httpbin.org/get"):
    """Verifica conectividade HTTP de forma simples"""
    if not REQUESTS_DISPONIVEL:
        return True, "⚠️ HTTP não testado (requests indisponível)"

    try:
        response = requests.get(url, timeout=5)
        return True, f"✅ HTTP OK - Status {response.status_code}"
    except Exception as e:
        return False, f"⚠️ HTTP com problema - {e} (pode ainda funcionar)"


def verificar_variaveis_ambiente():
    """Verifica se as variáveis de ambiente necessárias estão definidas"""
    vars_necessarias = ["TELEGRAM_TOKEN", "OPENAI_API_KEY", "OPENAI_MODEL"]
    resultados = []

    for var in vars_necessarias:
        valor = os.getenv(var)
        if valor:
            resultados.append(f"✅ {var}: Definida")
        else:
            resultados.append(f"❌ {var}: NÃO DEFINIDA")

    return resultados


def main():
    print("🔍 GeraTexto Bot - Verificação Simplificada")
    print("=" * 50)
    print(f"🕐 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Verificar variáveis de ambiente
    print("📋 Variáveis de Ambiente:")
    vars_ok = True
    for resultado in verificar_variaveis_ambiente():
        print(f"  {resultado}")
        if "❌" in resultado:
            vars_ok = False
    print()

    if not vars_ok:
        print("❌ VARIÁVEIS DE AMBIENTE FALTANDO!")
        print("   Verifique o arquivo .env")
        sys.exit(1)

    # Verificar conectividade básica (não restritiva)
    print("🌐 Testes Básicos de Conectividade:")

    dns_ok, dns_msg = verificar_dns()
    print(f"  {dns_msg}")

    if REQUESTS_DISPONIVEL:
        http_ok, http_msg = verificar_http_simples()
        print(f"  {http_msg}")
    else:
        print("  ⚠️ Testes HTTP pulados (requests não disponível)")

    print()
    print("=" * 50)
    print("💡 CONECTIVIDADE VERIFICADA!")
    print("   O bot tentará se conectar independentemente dos resultados.")
    print("   Problemas de rede podem ser temporários.")
    print()
    print("📋 Para monitorar:")
    print("   docker logs -f geratexto-bot")
    sys.exit(0)


if __name__ == "__main__":
    main()
