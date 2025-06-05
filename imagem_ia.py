from __future__ import annotations
import os
from pathlib import Path

import logging

from utils import verificar_env

from openai import OpenAI
import requests

verificar_env()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logger = logging.getLogger(__name__)


def gerar_imagem(prompt: str, destino: Path, tamanho: str = "1024x1024") -> Path:
    """Gera uma imagem usando a API da OpenAI e salva no caminho informado."""
    try:
        resposta = client.images.generate(
            model="dall-e-3", prompt=prompt, n=1, size=tamanho
        )
    except Exception:
        logger.exception("Erro ao chamar OpenAI images.generate")
        raise

    url = resposta.data[0].url
    img = requests.get(url, timeout=30).content
    destino.write_bytes(img)
    return destino


if __name__ == "__main__":
    from datetime import datetime

    p = Path("posts/teste.png")
    gerar_imagem("Robô programando em Python", p)
    print("Imagem salva em", p)
