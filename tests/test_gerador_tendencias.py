from unittest.mock import Mock, patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest

from gerador_tendencias import (
    HN_ITEM_URL,
    HN_TOP_URL,
    REDDIT_URL,
    TECHCRUNCH_RSS,
    Tendencia,
    obter_tendencias,
)


@patch('gerador_tendencias.TrendReq')
@patch('gerador_tendencias.requests.get')
def test_obter_tendencias(mock_get, mock_trendreq):
    """Testar agregação de tendências de todas as fontes."""

    # Preparar TrendReq.trending_searches
    mock_series = Mock()
    mock_series.tolist.return_value = ["Google1", "Google2"]
    mock_trendreq.return_value.trending_searches.return_value = [mock_series]

    def get_side_effect(url, *args, **kwargs):
        resp = Mock()
        if url == REDDIT_URL:
            resp.json.return_value = {
                "data": {
                    "children": [
                        {"data": {"title": "R1", "url": "http://r1"}},
                        {"data": {"title": "R2", "url": "http://r2"}},
                    ]
                }
            }
            return resp
        if url == HN_TOP_URL:
            resp.json.return_value = [101, 102]
            return resp
        if url == HN_ITEM_URL.format(101):
            resp.json.return_value = {"title": "HN101", "url": "http://hn101"}
            return resp
        if url == HN_ITEM_URL.format(102):
            resp.json.return_value = {"title": "HN102", "url": "http://hn102"}
            return resp
        if url == TECHCRUNCH_RSS:
            resp.content = (
                "<rss><channel>"
                "<item><title>Interesting Title One</title><link>http://t1</link></item>"
                "<item><title>Interesting Title Two</title><link>http://t2</link></item>"
                "</channel></rss>"
            ).encode()
            resp.raise_for_status = lambda: None
            return resp
        raise RuntimeError(f"URL inesperada: {url}")

    mock_get.side_effect = get_side_effect

    tendencias = obter_tendencias()
    titulos = [t.titulo for t in tendencias]

    esperado = {
        "Interesting Title One",
        "Interesting Title Two",
        "R1",
        "R2",
        "HN101",
        "HN102",
    }
    assert set(titulos) == esperado

from gerador_tendencias import gerar_resumo_tendencia, processar_tendencia_com_conteudo, Tendencia


def test_gerar_resumo_tendencia_curto():
    titulo = 'Titulo Curto'
    assert gerar_resumo_tendencia(titulo) == titulo


def test_processar_tendencia_com_conteudo():
    titulo = 'Titulo muito grande para testar o resumo automatico do codigo que deve truncar'
    tendencia = Tendencia(titulo, 'http://exemplo')
    res = processar_tendencia_com_conteudo(tendencia)
    assert res.titulo == titulo
    assert isinstance(res.resumo, str) and res.resumo
