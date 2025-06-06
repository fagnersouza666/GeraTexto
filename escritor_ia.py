from __future__ import annotations
import os
from datetime import datetime
from pathlib import Path
import re
import requests

import logging

from utils import verificar_env, obter_modelo_openai
from gerador_tendencias import extrair_texto_pagina

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
    prompt = f"{estilo}\n\nURL: {tema}"
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


def eh_url_valida(texto: str) -> bool:
    """Verifica se o texto é uma URL válida"""
    padrao_url = r"^https?://"
    return re.match(padrao_url, texto) is not None


def processar_url_para_post(url: str) -> tuple[str, str]:
    """
    Processa uma URL extraindo conteúdo e gerando resumo

    Returns:
        tuple: (titulo_sugerido, conteudo_resumido)
    """
    try:
        # Extrair conteúdo da página
        conteudo_completo = extrair_texto_pagina(url)

        if not conteudo_completo or len(conteudo_completo) < 50:
            raise Exception("Não foi possível extrair conteúdo suficiente da URL")

        # Usar a IA para criar um resumo inteligente do conteúdo
        prompt_resumo = f"""
Analise o seguinte conteúdo de uma página web e crie um resumo conciso e informativo:

CONTEÚDO:
{conteudo_completo[:4000]}  # Limitar para não exceder tokens

INSTRUÇÕES:
1. Identifique o assunto principal
2. Extraia os pontos mais importantes
3. Crie um resumo de 2-3 parágrafos (máximo 1000 palavras)
4. Mantenha o tom profissional, informativo e provocador
5. Foque nos aspectos mais relevantes e interessantes

RESUMO:
"""

        modelo = obter_modelo_openai()

        resposta = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt_resumo}],
            max_tokens=600,
        )

        resumo = resposta.choices[0].message.content.strip()

        # Gerar título sugerido baseado no resumo
        prompt_titulo = f"""
Baseado no seguinte resumo, sugira um título atrativo e informativo (máximo 60 caracteres):

RESUMO: {resumo[:500]}

TÍTULO SUGERIDO:
"""

        resposta_titulo = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt_titulo}],
            max_tokens=50,
        )

        titulo_sugerido = resposta_titulo.choices[0].message.content.strip()

        # Limpar título (remover aspas se houver)
        titulo_sugerido = titulo_sugerido.strip("\"'")

        return titulo_sugerido, resumo

    except Exception as e:
        logger.error(f"Erro ao processar URL {url}: {e}")
        raise Exception(f"Erro ao processar URL: {str(e)}")


def gerar_post_de_url(url: str) -> tuple[str, str]:
    """
    Gera post completo baseado em uma URL

    Returns:
        tuple: (titulo, post_completo)
    """
    try:
        titulo_sugerido, resumo = processar_url_para_post(url)

        # Gerar post usando o resumo como base
        estilo = _carregar_estilo()
        prompt = f"{estilo}\n\nConteúdo base (resumo de {url}):\n{resumo}\n\nCrie um post engajante baseado neste conteúdo:"
        modelo = obter_modelo_openai()

        resposta = client.chat.completions.create(
            model=modelo,
            messages=[{"role": "user", "content": prompt}],
        )

        texto = resposta.choices[0].message.content.strip()
        linhas = texto.splitlines()
        gancho = linhas[0] if linhas else ""
        corpo = "\n".join(linhas[1:]) if len(linhas) > 1 else ""

        template = _carregar_template()
        post_completo = template.render(titulo=titulo_sugerido, gancho=url, corpo=corpo)

        return titulo_sugerido, post_completo

    except Exception as e:
        logger.error(f"Erro ao gerar post de URL: {e}")
        raise


if __name__ == "__main__":
    import sys

    tema = " ".join(sys.argv[1:]) or "Inteligência Artificial"
    post = gerar_post(tema)
    arquivo = salvar_post(tema, post)
    print(f"Post salvo em {arquivo}")
