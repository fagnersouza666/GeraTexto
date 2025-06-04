import json
from dataclasses import dataclass
from typing import List
import requests
from pytrends.request import TrendReq

USER_AGENT = "GeraTextoBot/0.1"
REDDIT_URL = "https://www.reddit.com/r/artificial/hot.json?limit=10"
HN_TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
HN_ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

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
        return []


def tendencias_google(top_n: int = 5) -> List[Tendencia]:
    try:
        pt = TrendReq(hl="pt-BR", tz=360)
        trending = pt.trending_searches(pn="brazil")[0].tolist()
        return [Tendencia(t) for t in trending[:top_n]]
    except Exception:
        return []


def obter_tendencias() -> List[Tendencia]:
    temas: List[Tendencia] = []
    temas.extend(tendencias_reddit())
    temas.extend(tendencias_google())
    temas.extend(tendencias_hn())
    return temas


if __name__ == "__main__":
    for t in obter_tendencias():
        print("-", t.titulo)

