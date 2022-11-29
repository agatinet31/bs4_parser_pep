import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import BASE_DIR, MAIN_DOC_URL, PEPS_URL, TABLE_HEADER_WHATS_NEW, TABLE_HEADER_LATEST_VERSIONS, DOWNLOADS_DIR
from outputs import control_output
from utils import find_tag, find_tag_all, get_response, get_soup_by_url, download_file


def whats_new(session):
    """Возвращает информацию из раздела `Что нового`."""
    whats_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    soup = get_soup_by_url(session, whats_new_url)
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    sections_by_python = find_tag_all(
        div_with_ul, 'li', attrs={'class': 'toctree-l1'}
    )
    results = []
    for section in tqdm(sections_by_python):
        try:
            version_a_tag = find_tag(section, 'a', href=True)
            version_link = urljoin(whats_new_url, version_a_tag['href'])
            soup = get_soup_by_url(session, version_link)
            h1 = find_tag(soup, 'h1')
            dl = find_tag(soup, 'dl')
            dl_text = dl.text.replace('\n', ' ')
            results.append(
                (version_link, h1.text, dl_text)
            )
        except Exception:
            continue
    return [TABLE_HEADER_WHATS_NEW] + results if results else results


def latest_versions(session):
    """Возвращает список версий."""
    soup = get_soup_by_url(session, MAIN_DOC_URL)
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = find_tag_all(sidebar, 'ul')
    for ul in ul_tags:
        if 'All versions' in ul.text:
            a_tags = find_tag_all(ul, 'a', href=True)
            break
    else:
        raise Exception('С сервера возвращен пустой список версий!')
    results = []
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        version, status = (
                text_match.groups()
                if text_match else
                (a_tag.text, '')
        )
        results.append(
            (link, version, status)
        )
    return [TABLE_HEADER_LATEST_VERSIONS] + results if results else results


def download(session):
    """Загрузка файла с документацией."""
    downloads_url = urljoin(MAIN_DOC_URL, 'download.html')
    soup = get_soup_by_url(session, downloads_url)
    table_tag = find_tag(soup, 'table',  attrs={'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    archive_url = urljoin(downloads_url, pdf_a4_tag['href'])
    filename = archive_url.split('/')[-1]
    DOWNLOADS_DIR.mkdir(exist_ok=True)
    archive_path = DOWNLOADS_DIR / filename
    download_file(session, archive_url, archive_path)


def pep(session):
    """
    https://www.scrapingbee.com/blog/python-web-scraping-beautiful-soup/
    https://docs-python.ru/packages/paket-beautifulsoup4-python/css-selektory/
    https://www.crummy.com/software/BeautifulSoup/bs4/doc/#css-selectors

    https://thecode.media/try-except/
    https://docs.djangoproject.com/en/3.2/_modules/django/shortcuts/#get_object_or_404

    <a class="pep reference internal"
    href="/pep-0005" title="PEP 5 – Guidelines for Language Evolution">5</a>
    """
    soup = get_soup_by_url(session, PEPS_URL)
    section_numerical_index = find_tag(
            soup, 'section', {'class': 'numerical-index'}
    )
    pep_data = section_numerical_index.find_all(
            'a', {'class': 'pep reference internal'}
    )

    pep_url = MAIN_PEP_URL
    response = get_response(session, pep_url)
    if response is None:
        return None
    soup = BeautifulSoup(response.text, features='lxml')
    num_index = find_tag(soup, 'section', attrs={'id': 'numerical-index'})
    num_tbody = find_tag(num_index, 'tbody')
    num_trs = num_tbody.find_all('tr')
    results = {}
    total = 0
    for tr in tqdm(num_trs):
        status_key = find_tag(tr, 'td').text[1:]
        expected_status = EXPECTED_STATUS.get(status_key, [])
        if not expected_status:
            logging.info(f'Неизвестный ключ статуса: \'{status_key}\'')
        pep_link = urljoin(pep_url, find_tag(tr, 'a')['href'])
        response = get_response(session, pep_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, 'lxml')
        status = find_tag(soup, text='Status').find_next('dd').text
        if status not in expected_status:
            logging.info(
                f'Несовпадающие статусы: {pep_link} '
                f'Статус в карточке: {status} '
                f'Ожидаемые статусы: {expected_status}')
        results[status] = results.get(status, 0) + 1
        total += 1
    return (
        [('Статус', 'Количество')]
        + list(results.items())
        + [('Total', total)])


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep,
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу.')


if __name__ == '__main__':
    main()
