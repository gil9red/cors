#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import datetime as DT
import time
import uuid

from typing import Type, Optional, List

# pip install peewee
from peewee import Model, TextField, ForeignKeyField, CharField, DateTimeField, IntegerField, BooleanField
from playhouse.sqliteq import SqliteQueueDatabase

from config import DB_FILE_NAME, MAXIMUM_REQUESTS_PER_MONTH
from third_party.shorten import shorten


# This working with multithreading
# SOURCE: http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#sqliteq
db = SqliteQueueDatabase(
    DB_FILE_NAME,
    pragmas={
        'foreign_keys': 1,
        'journal_mode': 'wal',    # WAL-mode
        'cache_size': -1024 * 64  # 64MB page-cache
    },
    use_gevent=False,     # Use the standard library "threading" module.
    autostart=True,
    queue_max_size=64,    # Max. # of pending writes that can accumulate.
    results_timeout=5.0   # Max. time to wait for query to be executed.
)


class BaseModel(Model):
    """
    Базовая модель для классов-таблиц
    """

    class Meta:
        database = db

    def get_new(self) -> Type['BaseModel']:
        return type(self).get(self._pk_expr())

    @classmethod
    def get_first(cls) -> Type['BaseModel']:
        return cls.select().first()

    @classmethod
    def get_last(cls) -> Type['BaseModel']:
        return cls.select().order_by(cls.id.desc()).first()

    @classmethod
    def get_inherited_models(cls) -> List[Type['BaseModel']]:
        return sorted(cls.__subclasses__(), key=lambda x: x.__name__)

    @classmethod
    def print_count_of_tables(cls):
        items = []
        for sub_cls in cls.get_inherited_models():
            name = sub_cls.__name__
            count = sub_cls.select().count()
            items.append(f'{name}: {count}')

        print(', '.join(items))

    def __str__(self):
        fields = []
        for k, field in self._meta.fields.items():
            v = getattr(self, k)

            if isinstance(field, (TextField, CharField)):
                if v:
                    v = repr(shorten(v))

            elif isinstance(field, ForeignKeyField):
                k = f'{k}_id'
                if v:
                    v = v.id

            fields.append(f'{k}={v}')

        return self.__class__.__name__ + '(' + ', '.join(fields) + ')'


class ApiKey(BaseModel):
    value = TextField(unique=True, index=True)
    is_enabled = BooleanField(default=True)
    notes = TextField(null=True)
    created_date_time = DateTimeField(default=DT.datetime.now)

    @classmethod
    def add(cls, notes='') -> 'ApiKey':
        return cls.create(
            value=str(uuid.uuid4()),
            notes=notes,
        )

    @classmethod
    def get_by(cls, value: str) -> Optional['ApiKey']:
        return cls.get_or_none(value=value)

    @classmethod
    def is_exists(cls, value: str) -> bool:
        return cls.get_by(value) is not None

    def get_remained_requests_per_month(self) -> int:
        start_month = DT.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return MAXIMUM_REQUESTS_PER_MONTH - self.requests.where(Request.created_date_time >= start_month).count()

    def get_requests(self) -> List['Request']:
        return list(self.requests)


class Request(BaseModel):
    api_key = ForeignKeyField(ApiKey, backref='requests', null=True)
    client_ip = TextField()
    client_http_headers_json = TextField()
    url = TextField()
    url_domain = TextField(null=True)
    response_status_code = IntegerField(null=True)
    response_http_headers_json = TextField(null=True)
    our_status_code = IntegerField(null=True)
    our_decline_reason = TextField(null=True)
    created_date_time = DateTimeField(default=DT.datetime.now)


db.connect()
db.create_tables(BaseModel.get_inherited_models())

# Задержка в 50мс, чтобы дать время на запуск SqliteQueueDatabase и создание таблиц
# Т.к. в SqliteQueueDatabase запросы на чтение выполняются сразу, а на запись попадают в очередь
time.sleep(0.050)


if __name__ == '__main__':
    BaseModel.print_count_of_tables()
    print()

    if api_key := ApiKey.get_first():
        print(api_key.get_remained_requests_per_month())

        start_month = DT.datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        query = api_key.requests.where(Request.created_date_time >= start_month)
        for rq in query:
            print(rq)
