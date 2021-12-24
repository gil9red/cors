#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from pathlib import Path


# Текущая папка, где находится скрипт
DIR = Path(__file__).resolve().parent

# Создание папки для базы данных
DB_DIR_NAME = DIR / 'database'
DB_DIR_NAME.mkdir(parents=True, exist_ok=True)

# Путь к файлу базы данных
DB_FILE_NAME = str(DB_DIR_NAME / 'database.sqlite')

HEADER_REMAINED_REQUESTS = 'X-Remained-Requests'
HEADER_API_KEY = 'X-Api-Key'
IGNORED_RESPONSE_HEADERS = [
    'Content-Length', 'Transfer-Encoding', 'Content-Encoding'
]

PORT = 9999
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
MAXIMUM_REQUESTS_PER_MONTH = 10_000
