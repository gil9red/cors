#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from urllib.parse import urlparse

import requests

# pip install flask
from flask import Flask, request, Response

# pip install flask-cors
from flask_cors import CORS


# TODO: config.py
PORT = 9999

HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']
# TODO: ...
# HEADER_API_KEY = 'X-Api-Key'


app = Flask(__name__)
CORS(app)


@app.route("/<path:url_to>", methods=HTTP_METHODS)
def index(url_to: str):
    rq_headers = dict(request.headers)

    # TODO: возвращать 4xx с описанием ошибки, что-то типа: return 'bad request!', 400
    # if HEADER_API_KEY not in headers:

    # TODO: проверить наличие и ограничения
    # api_key = headers.pop(HEADER_API_KEY)

    url_parsed = urlparse(url_to)

    rq_headers['Host'] = url_parsed.netloc

    rs = requests.request(request.method, url_to, data=request.data, headers=rq_headers)
    rs_headers = dict(rs.headers)

    # TODO: завести список заголовков ответа, что нужно удалять
    # Удаление заголовков, которые могут повлиять на обработку ответа после возврата
    # Причина в том, что requests уже обработал ответ (например, если он был сжат) и
    # rs.content содержит ответ как есть
    rs_headers.pop('Content-Length', None)
    rs_headers.pop('Transfer-Encoding', None)
    rs_headers.pop('Content-Encoding', None)

    return Response(rs.content, rs.status_code, headers=rs_headers)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
