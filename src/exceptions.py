class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class DOMQueryingException(Exception):
    """Вызывается, когда парсер не может найти теги используя CSS селектор."""
    pass
