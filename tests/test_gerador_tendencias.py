from unittest.mock import Mock, patch

import pytest

from gerador_tendencias import (
    HN_ITEM_URL,
    HN_TOP_URL,
    REDDIT_URL,
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
        raise RuntimeError(f"URL inesperada: {url}")

    mock_get.side_effect = get_side_effect

    tendencias = obter_tendencias()
    titulos = [t.titulo for t in tendencias]

    assert titulos == ["R1", "R2", "Google1", "Google2", "HN101", "HN102"]
