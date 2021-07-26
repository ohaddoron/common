import typing as tp
import pymongo


def get_unique_patient_barcodes(col: pymongo.collection.Collection):
    """
    Fetches unique patient barcode values for a specific collection

    :param col: database collection handle
    :type col: pymongo.collection.Collection
    :return: list of unique barcode names
    :rtype: tp.List[str]
    """
    return col.find({}).distinct("bcr_patient_barcode")


def get_series_uids(col: pymongo.collection.Collection, patient_barcode: str):
    """
    Fetches uids for a specific patient barcode

    :param col:  database collection handle
    :type col: pymongo.collection.Collection
    :param patient_barcode: [unique identifier for a patient
    :type patient_barcode: str
    :return: series uids matching specific dicom images
    :rtype: tp.List[str]
    """
    return col.find({"bcr_patient_barcode": patient_barcode}).distinct("series_uid")
