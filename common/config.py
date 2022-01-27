from functools import lru_cache
import typing as tp
import os
from pathlib import Path

import toml


@lru_cache(maxsize=128)
def get_config(config_path: tp.Optional[str] = None, name: tp.Optional[str] = None):
    """
    Reads a configuration section for the configurtation file provided in config_path. If no section name is provided, will read the entire configuration file

    :param config_path: pathway to configuration file, if not provided will default to the local configuration path, defaults to None
    :type config_path: str
    :param name: section name, defaults to None
    :type name: tp.Optional[str], optional
    :return: requested configurations
    :rtype: dict
    """
    config_path = config_path or os.path.join(
        Path(__file__).parent, '../config.toml')
    with open(config_path) as f:
        config = toml.load(f)
    if name:
        return config[name]
    else:
        return config
