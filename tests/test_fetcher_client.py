from common.fetcher_client import *


def test_get_feature_names():
    assert isinstance(get_feature_names('GeneExpression'), list)


def test_get_patients_by_mutation():
    assert isinstance(get_patients_by_mutation('BRCA1', mutation_status=True), list)


def test_get_features_for_patients():
    assert isinstance(get_features_for_patients(col='GeneExpression', feature_name='BRCA1', patients=['TCGA-GM-A2DN']),
                      list)

    assert all([isinstance(item, dict) for item in
                get_features_for_patients(col='GeneExpression', feature_name='BRCA1',
                                          patients=get_patients_by_mutation('BRCA1', mutation_status=True))])


def test_get_patients_age():
    assert isinstance(get_patients_age(get_patients_by_mutation('BRCA1', mutation_status=True)), list)
    assert all(
        [isinstance(item, dict) for item in get_patients_age(get_patients_by_mutation('BRCA1', mutation_status=True))])
