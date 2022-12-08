from pathlib import Path

BASE_DIR = Path(__file__).parent

MAIN_DOC_URL = 'https://docs.python.org/3/'

PEPS_URL = 'https://peps.python.org/'

DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'

DT_FORMAT = '%d.%m.%Y %H:%M:%S'

LOG_PATH = BASE_DIR / 'logs'

LOG_FILE = LOG_PATH / 'parser.log'

LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'

DOWNLOADS_DIR = 'downloads'

EXPECTED_STATUS = {
    'A': ('Active', 'Accepted'),
    'D': ('Deferred',),
    'F': ('Final',),
    'P': ('Provisional',),
    'R': ('Rejected',),
    'S': ('Superseded',),
    'W': ('Withdrawn',),
    '': ('Draft', 'Active'),
}

VALID_STATUS = {
    status for statuses in EXPECTED_STATUS.values() for status in statuses
}

VERSION_AND_STATUS_PATTERN = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'

TABLE_HEADER_LATEST_VERSIONS = ('Ссылка на документацию', 'Версия', 'Статус')

TABLE_HEADER_WHATS_NEW = ('Ссылка на статью', 'Заголовок', 'Редактор, Автор')

TABLE_HEADER_STATUS_COUNT = ('Статус', 'Количество')

TABLE_FOOTER_STATUS_TOTAL = 'Total'
