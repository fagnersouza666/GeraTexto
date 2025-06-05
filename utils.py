from __future__ import annotations
import os
from dotenv import load_dotenv

REQUIRED_VARS = ("TELEGRAM_TOKEN", "OPENAI_API_KEY", "OPENAI_MODEL")


def verificar_env() -> None:
    """Garante que as variáveis de ambiente obrigatórias estejam presentes."""
    load_dotenv()
    faltantes = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if faltantes:
        nomes = ", ".join(faltantes)
        raise EnvironmentError(
            f"Defina as variáveis de ambiente {nomes} (.env ou sistema)."
        )


def obter_modelo_openai() -> str:
    """Retorna o modelo OpenAI configurado."""
    load_dotenv()
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
