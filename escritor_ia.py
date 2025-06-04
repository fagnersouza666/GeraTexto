from __future__ import annotations
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import logging
import openai
from jinja2 import Template

ESTILO_PATH = Path("prompts/estilo.txt")
TEMPLATE_PATH = Path("templates/artigo.md")
OUTPUT_DIR = Path("conteudos_gerados")

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)


def _carregar_estilo() -> str:
    return ESTILO_PATH.read_text(encoding="utf-8")


def _carregar_template() -> Template:
    return Template(TEMPLATE_PATH.read_text(encoding="utf-8"))


def gerar_post(tema: str) -> str:
    estilo = _carregar_estilo()
    prompt = f"{estilo}\n\nTema: {tema}"
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:
        logger.exception("Erro ao chamar OpenAI ChatCompletion")
        return ""
    texto = resposta["choices"][0]["message"]["content"].strip()
    linhas = texto.splitlines()
    gancho = linhas[0] if linhas else ""
    corpo = "\n".join(linhas[1:]) if len(linhas) > 1 else ""
    template = _carregar_template()
    return template.render(titulo=tema, gancho=gancho, corpo=corpo)


def salvar_post(tema: str, conteudo: str) -> Path:
    slug = "-".join(tema.lower().split())
    filename = datetime.now().strftime(f"%Y%m%d_%H%M%S_{slug}.md")
    OUTPUT_DIR.mkdir(exist_ok=True)
    caminho = OUTPUT_DIR / filename
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


if __name__ == "__main__":
    import sys

    tema = " ".join(sys.argv[1:]) or "Inteligência Artificial"
    post = gerar_post(tema)
    arquivo = salvar_post(tema, post)
    print(f"Post salvo em {arquivo}")

