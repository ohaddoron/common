import typing as tp
import pymongo
import SimpleITK as sitk
import numpy as np


def read_dicom_images(dicom_dir: str) -> np.ndarray:
    """
    Reads dicom images from a directories

    :param dicom_dir: pathway to a directory containing dicom files
    :type dicom_dir: str
    :return: array stack of dicom images
    :rtype: :class:`np.ndarray`
    """
    reader = sitk.ImageSeriesReader()
    dicom_names = reader.GetGDCMSeriesFileNames(dicom_dir)
    reader.SetFileNames(dicom_names)
    image = reader.Execute()
    nda = sitk.GetArrayFromImage(image)
    return nda
