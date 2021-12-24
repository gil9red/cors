#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


from db import ApiKey


api_key = ApiKey.add()
print(f'API-KEY: {api_key.value}')
