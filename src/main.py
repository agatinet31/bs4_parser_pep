import logging
import re
from collections import Counter
from urllib.parse import urljoin

import requests_cache
from tqdm import tqdm

from configs import configure_argument_parser, configure_logging
from constants import (BASE_DIR, DOWNLOADS_DIR, EXPECTED_STATUS, MAIN_DOC_URL,
                       PEPS_URL, TABLE_HEADER_LATEST_VERSIONS,
                       TABLE_HEADER_WHATS_NEW)
from outputs import control_output
from utils import (download_file, find_tag, find_tag_all, get_soup_by_url,
                   select_one_tag, select_tag_all)


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
    download_path = BASE_DIR / DOWNLOADS_DIR
    download_path.mkdir(exist_ok=True)
    archive_path = download_path / filename
    download_file(session, archive_url, archive_path)


def pep(session):
    """Возвращает количество PEP в каждом статусе."""
    soup = get_soup_by_url(session, PEPS_URL)       
    peps_records = select_tag_all(
        soup, '#numerical-index tbody > tr'
    )
    peps_status_count = {}
    for pep in tqdm(peps_records):
        try:
            href = find_tag(
                pep,
                'a',
                attrs={'class': 'pep reference internal', 'href': True}
            )['href']
            preview_status = select_one_tag(
                pep, 'tr:nth-child(1) > td:nth-child(1) > abbr'
            ).text[1:]
            pep_url = urljoin(PEPS_URL, href)
            pep_soup = get_soup_by_url(session, pep_url)            
            pep_status = select_one_tag(
                pep_soup, '#pep-content > dl > dd:nth-child(4) > abbr'
            ).text
            peps_status_count[pep_status] += 1
            preview_status = find_tag(pep, 'td').text[1:]
            if preview_status and EXPECTED_STATUS[] != :
            if status not in EXPECTED_STATUS:
                logging.info(UNEXPECTED_STATUSES.format(*item))
            """                        
            
            


            [
                ('Статус', 'Количество'),
                *sorted(results.items()),
                ('Total', sum(results.values())),
            ]
            """
        except Exception:
            continue        
    return None


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
