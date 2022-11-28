import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag_all(soup, tag=None, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
    """Поиск элементов по тегу."""
    searched_tag = soup.find_all(tag, attrs, recursive, text, limit, **kwargs)
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def find_tag(soup, tag=None, attrs={}, recursive=True, text=None,
             **kwargs):
    """Возвращает первый найденный элемент по тегу."""
    r = None
    l = find_tag_all(tag, attrs, recursive, text, 1, **kwargs)
    if l:
        r = l[0]
    return r

def get_soup_by_url(session, url):
    response = get_response(session, url)
    if response is None:
        return None
    return BeautifulSoup(response.text, features='lxml')
