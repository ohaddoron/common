# Created by ohad at 8/13/21
import os
from abc import ABC, abstractmethod

import PIL.Image
import numpy as np
from PIL import Image

from common.utils import read_dicom_images
import SimpleITK as sitk
import typing as tp
from loguru import logger
from common.les_files import read_all_maps_from_les_file


class ImageMaskHandlerBase(ABC):
    @staticmethod
    def read_image(path: str) -> sitk.Image:
        """
        Reads a stack of images from the provided path, outputs [width, height, slices]
        :param path: pathway to images to read
        :type path: str
        :return: Image stack
        :rtype: sitk.Image
        """
        raise NotImplementedError

    @staticmethod
    def read_masks(path: str, output_shape: tp.Tuple[int, int, int]) -> tp.List[sitk.Image]:
        """
        Reads all masks from the provided path into a list of SimpleITK images

        :param path: pathway to the location of the masks, can be a path to a file or a directory containing multiple masks, depending on the specific implementation
        :type path: str
        :param output_shape: output shape for the provided mask
        :param output_shape: Tuple[int, int int]
        :return: list of SimpleITK images
        :rtype: List[sitk.Image]
        """
        raise NotImplementedError

    @classmethod
    def read_image_and_mask(cls, path_to_images: str, path_to_mask: str) -> tp.Tuple[sitk.Image, tp.List[sitk.Image]]:
        """
        Reads both image and related segmentation masks
        :param path_to_images: pathway to images to read
        :type path_to_images: str
        :param path_to_mask: pathway to masks to read
        :type path_to_mask: str
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def overlay_mask_on_image(image: sitk.Image, mask: sitk.Image) -> PIL.Image.Image:
        raise NotImplementedError


class LESImageMaskHandler(ImageMaskHandlerBase):

    @staticmethod
    def read_image(path: str) -> sitk.Image:
        assert os.path.isdir(path), 'Provided path must be of a directory containing dicom images'
        return sitk.GetImageFromArray(read_dicom_images(path))

    @staticmethod
    def read_masks(path: str, output_shape: tp.Tuple[int, int, int]) -> tp.List[sitk.Image]:
        seg_maps = read_all_maps_from_les_file(path)

        masks = []
        for map in seg_maps:
            header = map['header']
            arr = np.zeros(output_shape, dtype=int)
            arr[header[2][0]: header[2][1] + 1, header[0][0]: header[0][1] + 1, header[1][0]: header[1][1] + 1] = map[
                'data']
            masks.append(sitk.GetImageFromArray(arr))

        return masks

    @classmethod
    def read_image_and_masks(cls, path_to_images: str, path_to_mask: str) -> tp.Tuple[sitk.Image, tp.List[sitk.Image]]:
        image = cls.read_image(path_to_images)
        masks = cls.read_masks(path_to_mask, image.GetSize()[::-1])
        return image, masks

    @staticmethod
    def overlay_mask_on_image(image: sitk.Image, mask: sitk.Image, alpha: float = 0.6, slice=0) -> PIL.Image.Image:
        image = sitk.GetArrayFromImage(image)[slice]
        image = 255. * (image / image.max())
        mask = sitk.GetArrayFromImage(mask)[slice] * 255

        image = np.array(Image.fromarray(image).convert('RGB'))

        image_2 = image.copy()

        image_2[..., 1] = np.maximum(image_2[..., 1], mask)

        result = ((1 - alpha) * image + alpha * image_2).astype(np.uint8)
        return Image.fromarray(result.astype(np.uint8))
