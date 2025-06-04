#!/usr/bin/env python3
"""
Script de teste para verificar se a instalação do GeraTexto está funcionando.
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Testa se todos os módulos podem ser importados."""
    print("🔍 Testando importações...")

    try:
        import bot_telegram

        print("✅ bot_telegram importado")
    except ImportError as e:
        print(f"❌ Erro ao importar bot_telegram: {e}")
        return False

    try:
        import escritor_ia

        print("✅ escritor_ia importado")
    except ImportError as e:
        print(f"❌ Erro ao importar escritor_ia: {e}")
        return False

    try:
        import imagem_ia

        print("✅ imagem_ia importado")
    except ImportError as e:
        print(f"❌ Erro ao importar imagem_ia: {e}")
        return False

    try:
        import gerador_tendencias

        print("✅ gerador_tendencias importado")
    except ImportError as e:
        print(f"❌ Erro ao importar gerador_tendencias: {e}")
        return False

    try:
        import utils

        print("✅ utils importado")
    except ImportError as e:
        print(f"❌ Erro ao importar utils: {e}")
        return False

    return True


def test_dependencies():
    """Testa se as dependências principais estão instaladas."""
    print("\n🔍 Testando dependências...")

    dependencies = [
        "telegram",
        "openai",
        "requests",
        "dotenv",
        "pytrends",
        "jinja2",
        "PIL",
    ]

    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} instalado")
        except ImportError:
            print(f"❌ {dep} não encontrado")
            return False

    return True


def test_directories():
    """Testa se os diretórios necessários existem."""
    print("\n🔍 Testando diretórios...")

    directories = ["posts", "templates"]

    for directory in directories:
        path = Path(directory)
        if path.exists():
            print(f"✅ Diretório {directory} existe")
        else:
            print(f"⚠️  Diretório {directory} não existe, criando...")
            path.mkdir(exist_ok=True)
            print(f"✅ Diretório {directory} criado")

    return True


def test_env_file():
    """Testa se o arquivo .env existe."""
    print("\n🔍 Testando arquivo .env...")

    env_path = Path(".env")
    if env_path.exists():
        print("✅ Arquivo .env existe")

        # Verificar se tem as variáveis necessárias
        with open(".env", "r") as f:
            content = f.read()

        if "TELEGRAM_TOKEN" in content:
            print("✅ TELEGRAM_TOKEN encontrado no .env")
        else:
            print("⚠️  TELEGRAM_TOKEN não encontrado no .env")

        if "OPENAI_API_KEY" in content:
            print("✅ OPENAI_API_KEY encontrado no .env")
        else:
            print("⚠️  OPENAI_API_KEY não encontrado no .env")

        return True
    else:
        print("⚠️  Arquivo .env não existe")
        print("💡 Execute: cp .env.example .env e configure suas chaves")
        return False


def main():
    """Executa todos os testes."""
    print("🚀 Iniciando testes de instalação do GeraTexto...\n")

    tests = [
        ("Importações", test_imports),
        ("Dependências", test_dependencies),
        ("Diretórios", test_directories),
        ("Arquivo .env", test_env_file),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))

    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)

    all_passed = True
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False

    print("=" * 50)

    if all_passed:
        print("🎉 Todos os testes passaram! O GeraTexto está pronto para uso.")
        print("\n📋 Próximos passos:")
        print("1. Configure o arquivo .env com suas chaves de API")
        print("2. Execute: python bot_telegram.py")
    else:
        print("⚠️  Alguns testes falharam. Verifique os erros acima.")
        print("\n💡 Dicas:")
        print("- Execute: ./install.sh para reinstalar")
        print("- Verifique se está no ambiente virtual: source .venv/bin/activate")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
