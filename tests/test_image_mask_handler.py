# Created by ohad at 8/13/21

from loguru import logger
from common.image_mask_reader import LESImageMaskHandler
import os
from PIL import Image
import numpy as np


class TestLESImageMaskHandler:
    def test_read_image_and_mask(self):
        handler = LESImageMaskHandler()

        image, masks = handler.read_image_and_mask(
            path_to_images=os.path.join(os.path.dirname(__file__), '../resources/dcm_files'),
            path_to_mask=os.path.join(os.path.dirname(__file__), '../resources/TCGA-AO-A0JI-1.les'))

        output = handler.overlay_mask_on_image(image, masks[0], slice=20)
        gt = Image.open(os.path.join(os.path.dirname(__file__), '../resources/read_image_and_mask_les.png'))

        np.testing.assert_array_almost_equal(np.array(output), np.array(gt))
