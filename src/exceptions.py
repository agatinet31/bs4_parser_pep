class ParserFindTagException(Exception):
    """Вызывается, когда парсер не может найти тег."""
    pass


class DOMQueryingException(Exception):
    """Вызывается, когда парсер не может найти теги используя CSS селектор."""
    pass


class PEPVersionException(Exception):
    """Вызывается, когда парсер возвращает пустой список версий."""
    pass


class PEPStatusException(Exception):
    """Вызывается, когда парсер возвращает невалидный статус."""
    pass
