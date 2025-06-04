from __future__ import annotations
import os
from pathlib import Path

from dotenv import load_dotenv
import logging

from utils import verificar_env

import openai
import requests

verificar_env()
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)


def gerar_imagem(prompt: str, destino: Path, tamanho: str = "512x512") -> Path:
    try:
        resposta = openai.Image.create(prompt=prompt, n=1, size=tamanho)
    except Exception:
        logger.exception("Erro ao chamar OpenAI Image.create")
        raise
    url = resposta["data"][0]["url"]
    img = requests.get(url, timeout=30).content
    destino.write_bytes(img)
    return destino


if __name__ == "__main__":
    from datetime import datetime

    p = Path("conteudos_gerados/teste.png")
    gerar_imagem("Robô programando em Python", p)
    print("Imagem salva em", p)

