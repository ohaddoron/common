# Created by ohad at 7/27/21
import os

import numpy as np
from common.utils import read_dicom_images
from loguru import logger


def test_read_dicom_images():
    dcm_images = read_dicom_images(os.path.join(os.path.dirname(__file__), "../resources/dcm_files"))
    assert isinstance(dcm_images, np.ndarray)
    assert dcm_images.shape == (34, 256, 256)
