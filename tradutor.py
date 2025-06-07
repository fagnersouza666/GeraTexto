import logging
from deep_translator import GoogleTranslator

_translator = GoogleTranslator(source="auto", target="pt")


def traduzir_para_pt(texto: str) -> str:
    """Traduz texto para português usando deep-translator."""
    try:
        return _translator.translate(texto)
    except Exception:
        logging.exception("Erro ao traduzir texto")
        return texto
