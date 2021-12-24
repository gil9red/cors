#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import json
from urllib.parse import urlparse

import requests

# pip install flask
from flask import Flask, request, Response, abort
from werkzeug.exceptions import HTTPException

# pip install flask-cors
from flask_cors import CORS

from config import HEADER_REMAINED_REQUESTS, HEADER_API_KEY, IGNORED_RESPONSE_HEADERS, PORT, HTTP_METHODS
import db


app = Flask(__name__)
CORS(app)


@app.route("/<path:url_to>", methods=HTTP_METHODS)
def index(url_to: str):
    url_parsed = urlparse(url_to)

    rq_db = db.Request()
    rq_db.client_ip = request.remote_addr
    rq_db.url = url_to
    rq_db.url_domain = url_parsed.netloc

    try:
        rq_headers = dict(request.headers)
        rq_db.client_http_headers_json = json.dumps(rq_headers, ensure_ascii=False)

        if HEADER_API_KEY not in rq_headers:
            abort(400, description='API-KEY is missing!')

        api_key_value = rq_headers.pop(HEADER_API_KEY)
        api_key = db.ApiKey.get(api_key_value)
        if not api_key:
            abort(401, description='Unknown API-KEY!')

        rq_db.api_key = api_key
        rq_headers['Host'] = rq_db.url_domain

        remained_requests = api_key.get_remained_requests_per_month()
        if remained_requests <= 0:
            abort(429, description='More requests this month are not allowed to be sent!')

        rs = requests.request(request.method, url_to, data=request.data, headers=rq_headers)

        rq_db.response_status_code = rs.status_code
        rq_db.response_http_headers_json = json.dumps(dict(rs.headers), ensure_ascii=False)

        # Удаление заголовков, которые могут повлиять на обработку ответа после возврата
        # Причина в том, что requests уже обработал ответ (например, если он был сжат) и
        # rs.content содержит ответ как есть
        for header in IGNORED_RESPONSE_HEADERS:
            rs.headers.pop(header, None)

        rs_header = dict(rs.headers)
        rs_header[HEADER_REMAINED_REQUESTS] = remained_requests

        rq_db.our_status_code = rs.status_code

        return Response(rs.content, rs.status_code, headers=rs_header)

    except Exception as e:
        if isinstance(e, HTTPException):
            rq_db.our_status_code = e.code
            rq_db.our_decline_reason = e.description

        raise e

    finally:
        rq_db.save()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
