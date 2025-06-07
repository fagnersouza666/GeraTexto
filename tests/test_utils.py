import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from unittest.mock import patch
import utils


def test_verificar_env_missing(monkeypatch):
    """Teste verificar_env com variáveis faltando"""
    # Remover variáveis de ambiente
    for var in utils.REQUIRED_VARS:
        monkeypatch.delenv(var, raising=False)

    # Mock do load_dotenv para não carregar .env real
    with patch("utils.load_dotenv"):
        with pytest.raises(EnvironmentError):
            utils.verificar_env()


def test_verificar_env_ok(monkeypatch):
    """Teste verificar_env com variáveis definidas"""
    # Definir todas as variáveis necessárias
    for var in utils.REQUIRED_VARS:
        monkeypatch.setenv(var, "test_value")

    # Mock do load_dotenv para usar apenas as variáveis do monkeypatch
    with patch("utils.load_dotenv"):
        utils.verificar_env()  # Não deve lançar exceção


def test_obter_modelo_openai(monkeypatch):
    """Teste obter_modelo_openai com e sem variável definida"""
    # Limpar variável e testar valor padrão
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    # Mock do load_dotenv para não carregar .env real
    with patch("utils.load_dotenv"):
        assert utils.obter_modelo_openai() == "gpt-4o-mini"

    # Definir variável customizada
    monkeypatch.setenv("OPENAI_MODEL", "custom-model")

    with patch("utils.load_dotenv"):
        assert utils.obter_modelo_openai() == "custom-model"
