import os
from glob import glob
from pathlib import Path

import pytest
from bson import json_util

from common.database import *
import mongoengine
import mongomock
from common.config import get_config
from mongoengine import disconnect


@pytest.fixture
def db_config():
    return dict(host='mongomock',
                user='mock',
                password='1234',
                port='27017',
                authentication_database='admin',
                db_name='mock')


def test_parse_connection_string(db_config: dict):
    connection_string = parse_mongodb_connection_string(**db_config)
    assert connection_string == 'mongodb://mock:1234@mongomock:27017/admin'


def test_init_cached_database():
    db = init_cached_database(
        connection_string='mongomock://localhost', db_name='mock', alias='mock')
    collections = db.list_collection_names()


def test_connect_to_database(db_config: dict):
    db = connect_to_database(db_config=db_config)
    assert db['segmentation_files'].find().alive
