from loguru import logger
import toml
from functools import lru_cache
import os
import typing as tp
from mongoengine import connect
from common.config import get_config


def parse_mongodb_connection_string(user: str, password: str, host: str, port: str, authentication_database: tp.Optional[str] = "admin", *args, **kwargs):
    """
    Parses a mongodb connection string from provided inputs

    :param user: name of the mongodb user
    :type user: str
    :param password: password for the requested mongodb user
    :type password: str
    :param host: mongodb host name
    :type host: str
    :param port: mongodb port
    :type port: str
    :param authentication_database: authentication database for the user, defaults to "admin"
    :type authentication_database: tp.Optional[str], optional
    :return: mongodb connection string
    :rtype: str
    """
    return f'mongodb://{user}:{password}@{host}:{port}/{authentication_database}'


@lru_cache
def init_cached_database(connection_string: str, db_name: str):
    """
    initializes a cahced handle to the mongodb database

    :param connection_string: mongodb connection string
    :type connection_string: str
    :param db_name: name of the database to connect to
    :type db_name: str
    :return: database handle
    :rtype: [type]
    """
    return connect(host=connection_string)[db_name]
