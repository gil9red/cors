#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import unittest

import requests

# TODO: test with all HTTP_METHODS
from config import PORT, HTTP_METHODS, HEADER_API_KEY

from db import ApiKey


if first := ApiKey.get_first():
    assert ApiKey.is_exists(first.value)

if last := ApiKey.get_last():
    assert ApiKey.is_exists(last.value)


# # These two lines enable debugging at httplib level (requests->urllib3->http.client)
# # You will see the REQUEST, including HEADERS and DATA, and RESPONSE with HEADERS but without DATA.
# # The only thing missing will be the response.body which is not logged.
# try:
#     import http.client as http_client
# except ImportError:
#     # Python 2
#     import httplib as http_client
# http_client.HTTPConnection.debuglevel = 1
#
# # You must initialize logging, otherwise you'll not see debug output.
# import logging
# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


# url_to = 'http://127.0.0.1:10016'
# url = f'http://10.7.8.31:{PORT}/{url_to}'
# headers = {
#     HEADER_API_KEY: ApiKey.get_first().value,
# }
#
# while True:
#     print(url)
#     rs = requests.get(url, headers=headers)
#
#     remained_requests = int(rs.headers.get('X-Remained-Requests', 0))
#     print(rs, remained_requests, rs.content.strip()[:100])
#     print()
#
#     rs.raise_for_status()
#     # quit()
#
#
# quit()

url_to = 'https://gist.github.com/gil9red/d56cc2085382d921789f73bd19e8f364'
# url_to = 'https://ya.ru'
url = f'http://localhost:{PORT}/' + url_to
print(url)
from urllib.parse import urlparse
headers = {
    # TODO: без HEADER_API_KEY
    # TODO: c HEADER_API_KEY
    # TODO: c неправильным HEADER_API_KEY
    HEADER_API_KEY: ApiKey.get_first().value,
    # HEADER_API_KEY: "<unknown>",
}
# TODO: сделать тест и проверить, что результат cors и обычного запроса одинаковый
# url = 'https://gist.github.com/gil9red/d56cc2085382d921789f73bd19e8f364'
rs = requests.get(url, headers=headers)
print(rs)
print(rs.headers)
print(rs.text.strip()[:100])
# print(rs.text.strip())

rs = requests.options(url, headers=headers)
print(rs)
print(rs.headers)
print(rs.text.strip()[:100])

# TODO: нужно еще статус код проверить
# TODO: нужно еще проверить заголовки ответа минус заголовки HEADER_REMAINED_REQUESTS и IGNORED_RESPONSE_HEADERS

# TODO: проверка идентичности ответов
# rs_direct = requests.get(url_to)
# print(rs_direct.text.strip()[:100])
# assert rs.text.strip()[:100] == rs_direct.text.strip()[:100]
