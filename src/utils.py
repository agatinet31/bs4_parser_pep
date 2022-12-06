import logging
import re

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import DOMQueryingException, ParserFindTagException


def get_response(session, url):
    """Загрузка данных ресурса по url."""
    try:
        response = session.get(url)
        response.raise_for_status()
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке ресурса по адресу: {url}',
            stack_info=True
        )
        raise


def download_file(session, url, file_path):
    """Загрузка файла по url."""
    response = get_response(session, url)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Файл был загружен и сохранён: {file_path}')


def get_soup_by_url(session, url):
    """Возвращает объект BeautifulSoup для страницы по url."""    
    response = get_response(session, url)
    response.encoding = 'utf-8'
    html = re.sub(r'>\s+<', '><', response.text.replace('\n', ''))    
    return BeautifulSoup(html, 'lxml')


def find_tag_all(soup, tag=None, *args, **kwargs):
    """Возвращает список элементов по тегу."""
    searched_tag = soup.find_all(tag, *args, **kwargs)
    if not searched_tag:
        attrs = kwargs.get('attrs', None)
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def find_tag(soup, tag=None, *args, **kwargs):
    """Возвращает первый найденный элемент по тегу."""
    tag_all = find_tag_all(soup, tag, *args, **kwargs)
    return tag_all[0] if tag_all else None


def select_tag_all(soup, selector, namespaces=None, limit=None, **kwargs):
    """Возвращает список элементов по CSS селектору."""
    select_tag = soup.select(selector, namespaces, limit, **kwargs)
    if not select_tag:
        error_msg = f'Не найдены теги по CSS селектору: {selector}'
        logging.error(error_msg, stack_info=True)
        raise DOMQueryingException(error_msg)
    return select_tag


def select_one_tag(soup, selector, namespaces=None, **kwargs):
    """"Возвращает первый элемент по выборке CSS селектора."""
    select_tag = select_tag_all(soup, selector, namespaces, 1, **kwargs)
    return select_tag[0] if select_tag else None
