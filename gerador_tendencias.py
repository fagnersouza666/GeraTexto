import logging
from dataclasses import dataclass
from typing import List
import requests
from pytrends.request import TrendReq
import re
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

USER_AGENT = "GeraTextoBot/0.1"
REDDIT_URL = "https://www.reddit.com/r/artificial/hot.json?limit=10"
HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
TECHCRUNCH_RSS = "https://techcrunch.com/tag/artificial-intelligence/feed/"


logger = logging.getLogger(__name__)


@dataclass
class Tendencia:
    titulo: str
    link: str | None = None
    resumo: str | None = None  # Novo campo para resumo do conteúdo


def extrair_texto_pagina(url: str) -> str:
    """Extrai texto principal de uma página web"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Extrair texto básico removendo HTML
        content = response.text

        # Remover scripts e styles
        content = re.sub(
            r"<script[^>]*>.*?</script>", "", content, flags=re.DOTALL | re.IGNORECASE
        )
        content = re.sub(
            r"<style[^>]*>.*?</style>", "", content, flags=re.DOTALL | re.IGNORECASE
        )

        # Remover tags HTML
        content = re.sub(r"<[^>]+>", " ", content)

        # Limpar espaços extras
        content = re.sub(r"\s+", " ", content)

        # Pegar os primeiros 500 caracteres de texto limpo
        texto_limpo = content.strip()[:500]

        return texto_limpo

    except Exception as e:
        logger.warning(f"Erro ao extrair conteúdo de {url}: {e}")
        return ""


def gerar_resumo_tendencia(titulo: str, conteudo: str = "") -> str:
    """Gera um resumo inteligente e conciso da tendência"""

    # Primeira tentativa: extrair palavras-chave do título
    palavras_titulo = titulo.lower().split()

    # Filtrar palavras relevantes do título
    stop_words = {
        "the",
        "a",
        "an",
        "and",
        "or",
        "but",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "by",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "being",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "that",
        "this",
        "its",
        "it",
        "since",
        "last",
        "more",
        "than",
        "times",
        "alleging",
    }

    palavras_importantes_titulo = [
        p for p in palavras_titulo if len(p) > 2 and p not in stop_words
    ]

    # Se o título é curto o suficiente, usar ele diretamente
    if len(titulo) <= 45:
        return titulo

    # Se tem palavras importantes do título, criar resumo com elas
    if palavras_importantes_titulo:
        # Pegar as 4-6 palavras mais importantes
        palavras_chave = " ".join(palavras_importantes_titulo[:6])
        if len(palavras_chave) > 40:
            palavras_chave = " ".join(palavras_importantes_titulo[:4])

        # Capitalizar primeira palavra
        if palavras_chave:
            palavras_chave = palavras_chave.capitalize()
            return palavras_chave

    # Fallback: truncar título de forma inteligente
    if len(titulo) > 45:
        # Tentar cortar em uma palavra completa
        truncado = titulo[:45]
        ultimo_espaco = truncado.rfind(" ")
        if ultimo_espaco > 20:  # Se tem espaço em posição razoável
            return titulo[:ultimo_espaco] + "..."
        else:
            return titulo[:45] + "..."

    return titulo


def processar_tendencia_com_conteudo(tendencia: Tendencia) -> Tendencia:
    """Processa uma tendência gerando resumo otimizado"""

    # Gerar resumo principalmente baseado no título (mais rápido e confiável)
    resumo = gerar_resumo_tendencia(tendencia.titulo)

    return Tendencia(titulo=tendencia.titulo, link=tendencia.link, resumo=resumo)


def tendencias_reddit(top_n: int = 5) -> List[Tendencia]:
    headers = {"User-Agent": USER_AGENT}
    try:
        resp = requests.get(REDDIT_URL, headers=headers, timeout=10)
        data = resp.json()
        topics = [
            Tendencia(child["data"]["title"], child["data"].get("url"))
            for child in data["data"]["children"]
        ]
        return topics[:top_n]
    except Exception:
        logger.exception("Erro ao obter tendências do Reddit")
        return []


def tendencias_hn(top_n: int = 5) -> List[Tendencia]:
    try:
        ids = requests.get(HN_TOP_URL, timeout=10).json()[:20]
        topics = []
        for i in ids:
            item = requests.get(HN_ITEM_URL.format(i), timeout=10).json()
            topics.append(Tendencia(item.get("title", ""), item.get("url")))
        return topics[:top_n]
    except Exception:
        logger.exception("Erro ao obter tendências do Hacker News")
        return []


def tendencias_techcrunch(top_n: int = 5) -> List[Tendencia]:
    """Obtém tendências do TechCrunch via RSS feed"""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(TECHCRUNCH_RSS, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse do XML RSS
        root = ET.fromstring(response.content)

        tendencias = []
        items = root.findall(".//item")[: top_n * 2]  # Pegar mais itens para filtrar

        for item in items:
            titulo_elem = item.find("title")
            link_elem = item.find("link")

            if titulo_elem is not None and link_elem is not None:
                titulo = titulo_elem.text.strip()
                link = link_elem.text.strip()

                # Filtrar títulos muito curtos ou genéricos
                if len(titulo) > 10 and not titulo.lower().startswith("techcrunch"):
                    # Limpar título se necessário
                    if titulo.endswith(" | TechCrunch"):
                        titulo = titulo[:-13]

                    tendencias.append(Tendencia(titulo, link))

                    if len(tendencias) >= top_n:
                        break

        logger.info(f"✅ TechCrunch: {len(tendencias)} tendências obtidas")
        return tendencias

    except Exception as e:
        logger.exception(f"Erro ao obter tendências do TechCrunch: {e}")
        return []


def tendencias_fallback() -> List[Tendencia]:
    """Tendências de fallback quando APIs externas falham"""
    return [
        Tendencia("Inteligência Artificial", "https://openai.com"),
        Tendencia("Python Programming", "https://python.org"),
        Tendencia("Machine Learning", "https://scikit-learn.org"),
        Tendencia("Tecnologia e Inovação", "https://github.com/trending"),
        Tendencia("Desenvolvimento Web", "https://developer.mozilla.org"),
        Tendencia("Automação de Processos", "https://www.python.org/"),
        Tendencia("Cloud Computing", "https://aws.amazon.com"),
        Tendencia("Cybersecurity", "https://www.cybersecurity.com"),
        Tendencia("ChatGPT e IA Generativa", "https://openai.com/chatgpt"),
        Tendencia("Blockchain e Criptomoedas", "https://bitcoin.org"),
        Tendencia("Realidade Virtual e Metaverso", "https://www.meta.com"),
        Tendencia("5G e Internet das Coisas", "https://www.ericsson.com"),
        Tendencia("Robótica e Drones", "https://robotics.org"),
        Tendencia("Startups e Empreendedorismo", "https://techcrunch.com"),
    ]


def obter_tendencias_por_fonte(fonte: int = 0) -> List[Tendencia]:
    """
    Obtém tendências de uma fonte específica

    Args:
        fonte (int):
            0 = Todas as fontes (padrão)
            1 = TechCrunch
            2 = Reddit
            3 = Hacker News
            4 = Tendências Fixas

    Returns:
        List[Tendencia]: Lista de tendências da fonte especificada
    """
    temas: List[Tendencia] = []

    if fonte == 1:  # Apenas TechCrunch
        logger.info("📰 Buscando tendências do TechCrunch...")
        try:
            temas = tendencias_techcrunch()
            if not temas:
                logger.warning("TechCrunch sem resultados, usando fallback")
                temas = tendencias_fallback()[:5]
        except Exception as e:
            logger.warning(f"TechCrunch indisponível: {e}")
            temas = tendencias_fallback()[:5]

    elif fonte == 2:  # Apenas Reddit
        logger.info("🔴 Buscando tendências do Reddit...")
        try:
            temas = tendencias_reddit()
            if not temas:
                logger.warning("Reddit sem resultados, usando fallback")
                temas = tendencias_fallback()[:5]
        except Exception as e:
            logger.warning(f"Reddit indisponível: {e}")
            temas = tendencias_fallback()[:5]

    elif fonte == 3:  # Apenas Hacker News
        logger.info("🍊 Buscando tendências do Hacker News...")
        try:
            temas = tendencias_hn()
            if not temas:
                logger.warning("Hacker News sem resultados, usando fallback")
                temas = tendencias_fallback()[:5]
        except Exception as e:
            logger.warning(f"Hacker News indisponível: {e}")
            temas = tendencias_fallback()[:5]

    elif fonte == 4:  # Apenas tendências fixas
        logger.info("📋 Usando tendências fixas...")
        temas = tendencias_fallback()[:5]

    else:  # fonte == 0 ou qualquer outro valor - todas as fontes
        return obter_tendencias()

    # Processar tendências
    logger.info("Processando tendências com conteúdo inteligente...")
    temas_processados = []

    for tema in temas[:5]:  # Limitar a 5 para fonte específica
        try:
            tema_processado = processar_tendencia_com_conteudo(tema)
            temas_processados.append(tema_processado)
        except Exception as e:
            logger.warning(f"Erro ao processar tendência {tema.titulo}: {e}")
            # Em caso de erro, usar a tendência original
            tema_limitado = Tendencia(
                titulo=(
                    tema.titulo[:50] + "..." if len(tema.titulo) > 50 else tema.titulo
                ),
                link=tema.link,
                resumo=(
                    tema.titulo[:50] + "..." if len(tema.titulo) > 50 else tema.titulo
                ),
            )
            temas_processados.append(tema_limitado)

    return temas_processados


def obter_tendencias() -> List[Tendencia]:
    temas: List[Tendencia] = []

    # Tentar TechCrunch
    try:
        techcrunch_trends = tendencias_techcrunch()
        if techcrunch_trends:
            temas.extend(techcrunch_trends)
    except Exception as e:
        logger.warning(f"TechCrunch indisponível: {e}")

    # Tentar Reddit
    temas.extend(tendencias_reddit())

    # Tentar Hacker News
    temas.extend(tendencias_hn())

    # Se não conseguiu nenhuma tendência, usar fallback
    if not temas:
        logger.info("Usando tendências de fallback")
        temas = tendencias_fallback()

    # Se ainda tem poucas tendências, complementar com fallback
    if len(temas) < 3:
        logger.info("Complementando com tendências de fallback")
        fallback_temas = tendencias_fallback()
        for tema in fallback_temas:
            if tema not in temas and len(temas) < 8:
                temas.append(tema)

    # Processar tendências para extrair conteúdo e gerar resumos
    logger.info("Processando tendências com conteúdo inteligente...")
    temas_processados = []

    for tema in temas[:8]:  # Limitar a 8 para não demorar muito
        try:
            tema_processado = processar_tendencia_com_conteudo(tema)
            temas_processados.append(tema_processado)
        except Exception as e:
            logger.warning(f"Erro ao processar tendência {tema.titulo}: {e}")
            # Em caso de erro, usar a tendência original com título limitado
            tema_limitado = Tendencia(
                titulo=(
                    tema.titulo[:50] + "..." if len(tema.titulo) > 50 else tema.titulo
                ),
                link=tema.link,
                resumo=(
                    tema.titulo[:50] + "..." if len(tema.titulo) > 50 else tema.titulo
                ),
            )
            temas_processados.append(tema_limitado)

    return temas_processados


if __name__ == "__main__":
    for t in obter_tendencias():
        print("-", t.titulo)
