from pathlib import Path
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import types
sys.modules['openai'] = types.SimpleNamespace(OpenAI=lambda api_key=None: types.SimpleNamespace())
os.environ.setdefault('TELEGRAM_TOKEN', 'x')
os.environ.setdefault('OPENAI_API_KEY', 'x')
os.environ.setdefault('OPENAI_MODEL', 'model')
from escritor_ia import eh_url_valida, salvar_post, salvar_texto_puro


def test_eh_url_valida():
    assert eh_url_valida('http://example.com')
    assert eh_url_valida('https://example.com')
    assert not eh_url_valida('notaurl')


def test_salvar_post(tmp_path, monkeypatch):
    monkeypatch.setattr('escritor_ia.OUTPUT_DIR', tmp_path)
    caminho = salvar_post('Tema Teste', 'conteudo')
    assert caminho.exists()
    assert caminho.read_text() == 'conteudo'
    assert caminho.parent == tmp_path


def test_salvar_texto_puro_remove_yaml(tmp_path, monkeypatch):
    monkeypatch.setattr('escritor_ia.OUTPUT_DIR', tmp_path)
    conteudo = '---\ntitle: Example\n---\n\nCorpo do post\n\n'
    caminho = salvar_texto_puro('Tema', conteudo)
    assert caminho.read_text() == 'Corpo do post'
