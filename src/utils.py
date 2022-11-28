import logging

from bs4 import BeautifulSoup
from requests import RequestException

from exceptions import ParserFindTagException


def get_response(session, url):
    """
    class:`Response` object
    if response.code is None:
            error_msg = f'Не найден тег {tag} {attrs}'
            logging.error(error_msg, stack_info=True)
            raise ParserFindTagException(error_msg)
            RequestException
    """
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )
        raise

    
def download_file(session, url, file_path):
    try:
        response = session.get(archive_url)
        with open(archive_path, 'wb') as file:
            file.write(response.content)
        logging.info(f'Архив был загружен и сохранён: {archive_path}')
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке архива {archive_url}',
            stack_info=True
        )


def find_tag_all(soup, tag=None, attrs={}, recursive=True, text=None,
                 limit=None, **kwargs):
    """Возвращает список элементов по тегу."""
    searched_tag = soup.find_all(tag, attrs, recursive, text, limit, **kwargs)
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def find_tag(soup, tag=None, attrs={}, recursive=True, text=None,
             **kwargs):
    """Возвращает первый найденный элемент по тегу."""
    return find_tag_all(tag, attrs, recursive, text, 1, **kwargs)[0]


def get_soup_by_url(session, url):
    response = get_response(session, url)
    return BeautifulSoup(response.text, features='lxml')
