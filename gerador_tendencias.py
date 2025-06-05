import logging
from dataclasses import dataclass
from typing import List
import requests
from pytrends.request import TrendReq

USER_AGENT = "GeraTextoBot/0.1"
REDDIT_URL = "https://www.reddit.com/r/artificial/hot.json?limit=10"
HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

logger = logging.getLogger(__name__)


@dataclass
class Tendencia:
    titulo: str
    link: str | None = None


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


def tendencias_google(top_n: int = 5) -> List[Tendencia]:
    try:
        pt = TrendReq(hl="pt-BR", tz=360)
        trending = pt.trending_searches(pn="brazil")[0].tolist()
        return [Tendencia(t) for t in trending[:top_n]]
    except Exception:
        logger.exception("Erro ao obter tendências do Google")
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
    ]


def obter_tendencias() -> List[Tendencia]:
    temas: List[Tendencia] = []

    # Tentar Reddit primeiro (mais confiável)
    temas.extend(tendencias_reddit())

    # Tentar Google Trends
    try:
        google_trends = tendencias_google()
        if google_trends:
            temas.extend(google_trends)
    except Exception as e:
        logger.warning(f"Google Trends indisponível: {e}")

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

    return temas


if __name__ == "__main__":
    for t in obter_tendencias():
        print("-", t.titulo)
