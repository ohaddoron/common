from common.database import init_cached_database, parse_mongodb_connection_string
import mongoengine
import mongomock
from common.config import get_config


def test_parse_connection_string():
    config = get_config(name='database')
    connection_string = parse_mongodb_connection_string(**config)
    pass


def test_init_cached_database():
    db = init_cached_database(
        connection_string='mongomock://localhost', db_name='mock')
