from common.config import get_config
import os


def test_get_config():
    assert get_config(os.path.join(os.path.dirname(__file__),
                                   '../config.toml'), 'test') == dict(test=True,
                                                                      database=dict(host='mongomock', user='mock',
                                                                                    password='1234', port='27017',
                                                                                    authentication_database='admin',
                                                                                    db_name='mock'))
