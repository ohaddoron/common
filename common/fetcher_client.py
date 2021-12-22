import httpx
import typing as tp
from loguru import logger
from pydantic import validate_arguments

ADDR = 'http://medical001-5.tau.ac.il/api'


def _perform_request(method: str, **params):
    with httpx.Client(timeout=None) as client:
        req = getattr(client, method)

        r = req(**params)
        r.raise_for_status()
    return r.json()


def get_features_for_patients(col: str, feature_name: str, patients: tp.List[str] = None) -> tp.List[dict]:
    return _perform_request(method='post', url=f'{ADDR}/features_for_patients',
                            json=dict(col=col, feature_name=feature_name, patients=patients)
                            )


def get_patients_by_mutation(mutation: str, mutation_status: bool) -> tp.List[str]:
    return _perform_request(method='get', url=f'{ADDR}/patients_by_mutation',
                            params=dict(mutation=mutation, mutation_status=mutation_status)
                            )


def get_patients_age(patients: tp.List[str]) -> tp.List[dict]:
    return _perform_request(method='post', url=f'{ADDR}/patients_age', json=patients)


def get_feature_names(col: str) -> tp.List[str]:
    return _perform_request('get', url=f'{ADDR}/feature_names', params=dict(col=col))
