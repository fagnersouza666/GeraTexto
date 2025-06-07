import asyncio
import types
from unittest.mock import AsyncMock, MagicMock, patch
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import healthcheck


def test_verificar_variaveis(monkeypatch):
    monkeypatch.setenv("TELEGRAM_TOKEN", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "2")
    ok, msg = healthcheck.verificar_variaveis()
    assert ok is True


def test_verificar_variaveis_faltando(monkeypatch):
    monkeypatch.delenv("TELEGRAM_TOKEN", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "2")
    ok, msg = healthcheck.verificar_variaveis()
    assert not ok
    assert "TELEGRAM_TOKEN" in msg


def test_verificar_bot_simples(monkeypatch):
    """Teste verificar_bot_simples com mock do Bot"""
    monkeypatch.setenv("TELEGRAM_TOKEN", "1")
    dummy = types.SimpleNamespace(Bot=MagicMock())
    with patch.dict("sys.modules", {"telegram": dummy}):
        instance = dummy.Bot.return_value
        instance.get_me = AsyncMock(return_value=types.SimpleNamespace(username="bot"))

        # Usar asyncio.run() ao invés de get_event_loop() deprecated
        ok, msg = asyncio.run(healthcheck.verificar_bot_simples())
        assert ok
        assert "@bot" in msg
        instance.get_me.assert_called_once()
