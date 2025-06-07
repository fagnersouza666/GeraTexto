import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
import utils


def test_verificar_env_missing(monkeypatch):
    for var in utils.REQUIRED_VARS:
        monkeypatch.delenv(var, raising=False)
    with pytest.raises(EnvironmentError):
        utils.verificar_env()


def test_verificar_env_ok(monkeypatch):
    for var in utils.REQUIRED_VARS:
        monkeypatch.setenv(var, 'x')
    utils.verificar_env()


def test_obter_modelo_openai(monkeypatch):
    monkeypatch.delenv('OPENAI_MODEL', raising=False)
    assert utils.obter_modelo_openai() == 'gpt-4o-mini'
    monkeypatch.setenv('OPENAI_MODEL', 'custom')
    assert utils.obter_modelo_openai() == 'custom'
