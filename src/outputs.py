import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT


def default_output(results, *args):
    """Дефолтный вывод в консоль."""
    print(
        '\n'.join(
            ' '.join(value) for value in results
        )
    )


def pretty_output(results, *args):
    """Вывод результата в виде таблицы."""
    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    """Запись результатов в файл."""
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


OUTPUT_TO_FUNCTION = {
    'pretty': pretty_output,
    'file': file_output,
    'console': default_output,
}


def control_output(results, cli_args):
    OUTPUT_TO_FUNCTION.get(cli_args.output, default_output)(results, cli_args)
