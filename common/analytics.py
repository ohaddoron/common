import os
from concurrent.futures import ProcessPoolExecutor

from common.fetcher_client import get_patients_by_mutation
from common.fetcher_client import get_patients_age, get_features_for_patients, get_feature_names
import typing as tp

from scipy.stats import ks_2samp


def get_patients_split(mutation, mutation_status, age_cutoff=45):
    patients = get_patients_by_mutation(mutation=mutation, mutation_status=mutation_status)
    patients_ages = get_patients_age(patients=patients)

    early = [item['patient'] for item in patients_ages if item['age'] < age_cutoff]
    late = [item['patient'] for item in patients_ages if item['age'] >= age_cutoff]
    return early, late


def significance_test(patients_1: tp.List[str], patients_2: tp.List[str], feature: str, col: str, mutation: str,
                      mutation_status: bool) -> dict:
    data_1 = [item['value'] for item in
              get_features_for_patients(col=col, feature_name=feature, patients=patients_1)]
    data_2 = [item['value'] for item in
              get_features_for_patients(col=col, feature_name=feature, patients=patients_2)]
    return dict(mutation=mutation, mutation_status=mutation_status, feature_name=feature,
                pvalue=float(ks_2samp(data1=data_1, data2=data_2).pvalue))


def analyze_bundle(mutation: str, mutation_status: bool, col: str, age_cutoff: int = 45) -> tp.List[dict]:
    """
    Computes p values for the null hypothesis where the distribution of the early onset patients and the late onset
    patients is the same for some given feature. This computation is performed for all features in a specific
    "bundle", called col here

    :param mutation: mutated gene. will split the population according to the requested gene (along with age cutoff)
    :param mutation_status: if True, will use mutated patients
    :param col: "bundle" to analyze
    :return: list of dictionaries containing pvalues and feature name
    """
    feature = get_feature_names(col)

    early, late = get_patients_split(mutation=mutation, mutation_status=mutation_status, age_cutoff=age_cutoff)

    n_features = len(feature)
    with ProcessPoolExecutor(max_workers=os.cpu_count()) as executor:
        results = list(
            executor.map(significance_test, [early] * n_features, [late] * n_features,
                         feature, [col] * n_features, [mutation] * n_features, [mutation_status] * n_features)
        )

    return results
