from common.les_files import *
from loguru import logger
import os
import pytest
import pickle as pkl
import numpy as np


@pytest.fixture(scope='module')
def arr():
    path = os.path.join(os.path.dirname(__file__),
                        '../resources/TCGA-AO-A0JI-1.les')
    with open(path, 'rb') as f:
        arr = f.read()
    return arr


def test_read_les_file_header(arr):
    header = read_les_file_header(arr)
    assert header == [(99, 114), (115, 128), (19, 22)]


def test_read_les_file_data(arr):
    header = read_les_file_header(arr)

    data = read_les_file_data(arr, header, offset=12)

    with open(os.path.join(os.path.dirname(__file__), '../resources/les_file_image.pkl'), 'rb') as f:
        gt = pkl.load(f)

    np.testing.assert_array_equal(gt, data)


def test_read_les_file_data_raises_for_offset_too_small(arr):
    header = read_les_file_header(arr)

    with pytest.raises(AssertionError):
        read_les_file_data(arr, header, offset=0)


def test_read_all_maps_from_les_file():

    path = os.path.join(os.path.dirname(__file__),
                        '../resources/TCGA-E2-A1IJ-1.les')

    maps = read_all_maps_from_les_file(path=path)
