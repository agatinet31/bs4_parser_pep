# Парсер документации python
Парсер документации python c https://docs.python.org/3/ и https://peps.python.org/

## Содержание
- [Технологии](#технологии)
- [Использование](#использование)
- [Над проектом работали](#над-проектом-работали)

## Технологии
- [Python](https://www.python.org/)
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)

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
Парсер запускается из папки ./src/
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
Парсит спсок изменений python
#### latest_versions:
Парсит список версий python и ссылки на документацию
#### download:
Cкачивает архив с документацией в папку ./downloads
#### pep:
Парсит список статусов документов pep и подсчитывает количество документов для каждого статуса
### Способы вывода данных:
#### pretty:
Выводит данные в терминал в виде таблицы
#### file:
Сохраняет данные в папке ./results в формате csv
