import numpy as np
from typing import List, Tuple

from loguru import logger


def read_les_file_header(arr, offset=0):
    """
    Reads a "header" of a les file. The header is composed of 6 uint16 values (12 bytes) and defines a cuboid in which a lesion exists

    :param arr: bytes array containing raw bytes for the entire segementation map
    :type arr: bytes
    :param offset: offset value to read from the begining of the bytes array, defaults to 0
    :type offset: int, optional
    :return: list of starting and ending position pairs, ordered as (y, x, z)
    :rtype: List[List[int]]
    """
    arr = np.array([int.from_bytes(arr[i: i + 2], 'little', signed=False)
                    for i in range(0, 12, 2)]).reshape(2, 3)
    assert min(arr[1] - arr[0]
               ), 'max values must be greater than min values in header'

    # returns ((ymin, ymax), (xmin, xmax), (zmin, zmax))
    return [tuple(arr[:, 0]), tuple(arr[:, 1]), tuple(arr[:, 2])]


def _get_data_length(header: List[Tuple[int, int]]):
    return np.prod([(item[1] - item[0] + 1) for item in header])


def _get_data_shape(header: List[Tuple[int, int]]):
    return (header[2][1] - header[2][0] + 1,
            header[1][1] - header[1][0] + 1,
            header[0][1] - header[0][0] + 1)


def read_les_file_data(arr, header: List[Tuple[int, int]], offset=12):
    """
    Reads data associated with a single header and following a specific offset. The minimal offset is 12 bytes, corresponding to the length of the first header

    :param arr: raw bytes array of a les file
    :type arr: bytes
    :param header: header of the current segmentation map
    :type header: List[Tuple[int, int]]
    :param offset: offset value from which the reading should begin, defaults to 12
    :type offset: int, optional
    :return: 3D array corresponding to different slices of the segmentation map
    :rtype: np.array
    """

    assert offset >= 12, 'offset must be greater than 12 bytes, the length of the first header in the file'
    assert len(arr[offset: offset + _get_data_length(header)]
               ) == _get_data_length(header), 'number of bytes to read must the length defined by the header'

    shape = _get_data_shape(header)

    return np.array([item for item in arr[offset: offset + _get_data_length(header)]]).reshape(shape)


def read_all_maps_from_les_file(path: str):
    offset = 0

    segmentation_maps = []
    with open(path, 'rb') as f:
        arr = f.read() 

    while True:
        if offset == len(arr):
            return segmentation_maps

        # read header of the current offset
        header = read_les_file_header(arr, offset=offset)
        # update offset according to the number of bytes in a header
        offset += 12

        data = read_les_file_data(arr, header, offset=offset)

        segmentation_maps.append(data)

        offset += _get_data_length(header)
