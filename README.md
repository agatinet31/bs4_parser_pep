# Парсер информации по Python и PEP документации
Парсер формирует информацию по версиям Python cо страницы https://docs.python.org/3/ и краткую информацию документации PEP по их статусам и количествам со страницы https://peps.python.org/

## Использование
Склонируйте репозиторий  
Создайте виртуальное окружение 
```
python -m venv venv
```
Активируйте виртуальное окружение  
Установить зависимости 
```
pip install -r requirements.txt
```
Парсер запускается из директории src
```
usage: main.py [-h] [-c] [-o {pretty,file}] {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
### Режимы работы:
#### whats-new:
Формирует список изменений Python
#### latest_versions:
Формирует список версий Python c ссылками на документацию
#### download:
Загружает архив с документацией в директорию downloads
#### pep:
Формирует по документации PEP список статусов и их количество
### Способы вывода данных:
#### pretty:
Выводит результат в виде таблицы
#### file:
Сохраняет данные в формате csv в директорию results

## Автор
Андрей Лабутин