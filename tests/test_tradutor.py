from unittest.mock import MagicMock, patch
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tradutor import traduzir_para_pt


@patch('tradutor._translator')
def test_traduzir_para_pt(mock_trans):
    mock_trans.translate.return_value = 'Olá'
    assert traduzir_para_pt('Hello') == 'Olá'
    mock_trans.translate.assert_called_once_with('Hello')


@patch('tradutor._translator')
def test_traduzir_erro_retorna_original(mock_trans):
    mock_trans.translate.side_effect = Exception('fail')
    texto = 'Hello'
    assert traduzir_para_pt(texto) == texto
