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


def test_parse_connection_string():
    config = get_config(name='test')['database']
    connection_string = parse_mongodb_connection_string(**config)
    assert connection_string == 'mongodb://mock:1234@mongomock:27017/admin'


def test_init_cached_database():
    db = init_cached_database(
        connection_string='mongomock://localhost', db_name='mock', alias='mock')
    collections = db.list_collection_names()


def test_init_cached_database_no_inputs():
    db = init_cached_database()
    collections = db.list_collection_names()


def test_connect_to_database():
    db = connect_to_database()
    assert db['segmentation_files'].find().alive


def test_get_segmentation_files():
    segmentation_files = get_segmentation_files('TCGA-AO-A12D')
    assert isinstance(segmentation_files, list)


def test_get_dcm_dirs():
    dcm_dirs = get_dcm_dirs('TCGA-AO-A12D')
    assert isinstance(dcm_dirs, list)
