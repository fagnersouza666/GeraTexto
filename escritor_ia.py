from __future__ import annotations
import os
from datetime import datetime
from pathlib import Path

import logging

from utils import verificar_env, obter_modelo_openai

from openai import OpenAI
from jinja2 import Template

BASE_DIR = Path(__file__).resolve().parent
ESTILO_PATH = BASE_DIR / "prompts" / "estilo.txt"
TEMPLATE_PATH = BASE_DIR / "templates" / "artigo.md"
OUTPUT_DIR = BASE_DIR / "posts"

verificar_env()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logger = logging.getLogger(__name__)


def _carregar_estilo() -> str:
    """Carrega o prompt de estilo utilizado na geração do texto."""
    return ESTILO_PATH.read_text(encoding="utf-8")


def _carregar_template() -> Template:
    """Carrega o template Markdown do post."""
    return Template(TEMPLATE_PATH.read_text(encoding="utf-8"))


def gerar_post(tema: str) -> str:
    """Gera o texto do post a partir de um tema utilizando a API da OpenAI."""
    estilo = _carregar_estilo()
    prompt = f"{estilo}\n\nTema: {tema}"
    modelo = obter_modelo_openai()

    try:
        resposta = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception:
        logger.exception("Erro ao chamar OpenAI ChatCompletion")
        return ""

    texto = resposta.choices[0].message.content.strip()
    linhas = texto.splitlines()
    gancho = linhas[0] if linhas else ""
    corpo = "\n".join(linhas[1:]) if len(linhas) > 1 else ""
    template = _carregar_template()
    return template.render(titulo=tema, gancho=gancho, corpo=corpo)


def salvar_post(tema: str, conteudo: str) -> Path:
    """Salva o conteúdo em arquivo Markdown e retorna o caminho criado."""
    # Limitar o slug para evitar nomes de arquivo muito longos
    # Isso evita problemas com callback_data > 64 bytes
    slug = "-".join(tema.lower().split())

    # Limitar slug a 30 caracteres para garantir nome de arquivo seguro
    if len(slug) > 30:
        # Pegar palavras importantes e limitar
        palavras = slug.split("-")
        slug_limitado = ""
        for palavra in palavras:
            if len(slug_limitado + palavra + "-") <= 30:
                slug_limitado += palavra + "-"
            else:
                break
        slug = slug_limitado.rstrip("-")

        # Se ainda está vazio, usar apenas as primeiras letras
        if not slug:
            slug = tema.lower().replace(" ", "")[:30]

    filename = datetime.now().strftime(f"%Y%m%d_%H%M%S_{slug}.md")
    OUTPUT_DIR.mkdir(exist_ok=True)
    caminho = OUTPUT_DIR / filename
    caminho.write_text(conteudo, encoding="utf-8")
    return caminho


def salvar_texto_puro(tema: str, conteudo: str) -> Path:
    """Salva apenas o conteúdo do post em arquivo .txt para fácil cópia"""
    # Limitar o slug para evitar nomes de arquivo muito longos
    slug = "-".join(tema.lower().split())

    # Limitar slug a 30 caracteres
    if len(slug) > 30:
        palavras = slug.split("-")
        slug_limitado = ""
        for palavra in palavras:
            if len(slug_limitado + palavra + "-") <= 30:
                slug_limitado += palavra + "-"
            else:
                break
        slug = slug_limitado.rstrip("-")

        if not slug:
            slug = tema.lower().replace(" ", "")[:30]

    filename = datetime.now().strftime(f"%Y%m%d_%H%M%S_{slug}.txt")
    OUTPUT_DIR.mkdir(exist_ok=True)
    caminho_txt = OUTPUT_DIR / filename

    # Extrair apenas o conteúdo do post (sem metadados YAML)
    linhas = conteudo.split("\n")
    texto_limpo = []

    # Encontrar e pular o bloco YAML frontmatter
    yaml_start_found = False
    yaml_end_found = False

    for linha in linhas:
        # Se encontrou o primeiro ---, está no início do YAML
        if linha.strip() == "---" and not yaml_start_found:
            yaml_start_found = True
            continue
        # Se encontrou o segundo ---, está no fim do YAML
        elif linha.strip() == "---" and yaml_start_found and not yaml_end_found:
            yaml_end_found = True
            continue
        # Se já passou do YAML ou não tem YAML, incluir a linha
        elif yaml_end_found or not yaml_start_found:
            texto_limpo.append(linha)

    # Limpar linhas vazias do início e fim
    while texto_limpo and not texto_limpo[0].strip():
        texto_limpo.pop(0)
    while texto_limpo and not texto_limpo[-1].strip():
        texto_limpo.pop()

    # Unir as linhas
    texto_final = "\n".join(texto_limpo)

    caminho_txt.write_text(texto_final, encoding="utf-8")
    return caminho_txt


if __name__ == "__main__":
    import sys

    tema = " ".join(sys.argv[1:]) or "Inteligência Artificial"
    post = gerar_post(tema)
    arquivo = salvar_post(tema, post)
    print(f"Post salvo em {arquivo}")
