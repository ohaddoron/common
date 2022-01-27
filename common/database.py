import os
import typing as tp
from functools import lru_cache
from pathlib import Path
from uuid import uuid4

import motor
import pymongo.database
from mongoengine import connect
import motor.motor_asyncio


def parse_mongodb_connection_string(user: str, password: str, host: str, port: str,
                                    authentication_database: tp.Optional[str] = "admin", *args, **kwargs) -> str:
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


@lru_cache(maxsize=128)
def init_cached_database(connection_string: str, db_name: str,
                         alias: tp.Optional[str] = None, async_flag=False) -> tp.Union[
    pymongo.database.Database]:
    """
    initializes a cahced handle to the mongodb database

    :param connection_string: mongodb connection string
    :type connection_string: str
    :param db_name: name of the database to connect to
    :type db_name: str
    :return: database handle
    :rtype: :class:`pymongo.database.Database`
    """
    alias = alias or uuid4().hex
    if not async_flag:
        return connect(host=connection_string, alias=alias)[db_name]
    else:
        return motor.motor_asyncio.AsyncIOMotorClient(host=connection_string)[db_name]


def connect_to_database(db_config: dict) -> pymongo.database.Database:
    """
    Connection to database method accepting a dictionary for database configuration

    >>> db_config = dict(host='mongomock', user='mock', password='1234', port='27017', authentication_database='admin', db_name='mock')
    >>> db = connect_to_database(db_config)

    :param db_config: database configuration dictionary
    :type db_config: dict
    :return: DB handle instance
    :rtype: :class:`pymongo.database.Database`
    """
    return init_cached_database(parse_mongodb_connection_string(
        **db_config), db_name=db_config['db_name'])


@lru_cache
def init_database(config_name: str, async_flag: bool = False, config_path=None):
    from common.config import get_config
    config_path = config_path or Path(Path(__file__).parent, '../config.toml').as_posix()
    config = get_config(config_path=config_path, name=config_name)
    db = init_cached_database(parse_mongodb_connection_string(
        **config), db_name=config['db_name'], async_flag=async_flag)
    return db


def fetch_collection_as_table(col: str, patients: tp.List[str] = None, **params):
    db = init_database(**params)

    return db[col].aggregate([
        {
            "$match": {
                "patient": {"$in": patients}
            }
        } if patients else {"$match": {}},
        {
            '$group': {
                '_id': '$sample',
                'data': {
                    '$push': {
                        'k': '$name',
                        'v': '$value'
                    }
                },
                'patient': {
                    '$push': '$patient'
                }
            }
        }, {
            '$project': {
                'patient': {
                    '$arrayElemAt': [
                        '$patient', 0
                    ]
                },
                'sample': '$_id',
                '_id': 0,
                'data': {
                    '$arrayToObject': '$data'
                }
            }
        }, {
            '$replaceRoot': {
                'newRoot': {
                    '$mergeObjects': [
                        '$$ROOT', '$data'
                    ]
                }
            }
        }, {
            '$project': {
                'data': 0
            }
        }
    ],
        allowDiskUse=True)
