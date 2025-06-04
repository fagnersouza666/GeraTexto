from __future__ import annotations
import os
import sys
from dotenv import load_dotenv


def verificar_env() -> None:
    """Verifica se as variáveis necessárias estão definidas.

    Exige TELEGRAM_TOKEN e OPENAI_API_KEY. Caso alguma esteja ausente,
    uma mensagem amigável é exibida e o programa é encerrado.
    """
    load_dotenv()
    faltantes = [var for var in ("TELEGRAM_TOKEN", "OPENAI_API_KEY") if not os.getenv(var)]
    if faltantes:
        nomes = ", ".join(faltantes)
        print(
            f"Erro: defina as variáveis de ambiente {nomes} "
            "(arquivo .env ou variáveis do sistema)."
        )
        sys.exit(1)

