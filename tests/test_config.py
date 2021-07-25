from common.config import get_config
import os


def test_get_config():
    assert get_config(os.path.join(os.path.dirname(__file__),
                      '../config.toml'), 'test') == {'test': True}
