import numpy as np

from mapof.elections.objects import Election

from mapof.elections.distances.register import register_ordinal_election_distance


def _feature_distance(e1: Election, e2: Election, feature_ids: list[str], ord: int):
    """ L1 or L2 distance between two feature vectors """
    vector_1 = []
    vector_2 = []
    for feature_id in feature_ids:
        try:
            vector_1.append(e1.get_feature[feature_id], compute_if_missing=False)
            vector_2.append(e2.get_feature[feature_id], compute_if_missing=False)
        except Exception:
            raise Exception(f"Feature {feature_id} not found in the election objects")
    return np.linalg.norm(vector_1 - vector_2, ord=ord)


@register_ordinal_election_distance("feature_l1")
def features_vector_l1(e1: Election, e2: Election, feature_ids: list[str]):
    """ L1 distance between two feature vectors """
    return _feature_distance(e1, e2, feature_ids, 1)


@register_ordinal_election_distance("feature_l2")
def features_vector_l2(e1: Election, e2: Election, feature_ids: list[str]):
    """ L2 distance between two feature vectors """
    return _feature_distance(e1, e2, feature_ids, 2)


"""
Sample driver function of the feature distance.

For successful calculation the features you decide to use need to be loaded into memory for example as follows:

experiment.features["Agreement"] = experiment.import_feature("AgreementApprox")

Then the prepare_feature_vectors function allows to pick which features will be used - codes of the features need to be passed as a list.
Currently supported feature codes are the following:
d := Diversity
a := Agreement
p := Polarization
e := Entropy
e2 := Entropy squared

Example usage which selects DAP features:
experiment.prepare_feature_vectors(['d', 'a', 'p'])
Any number of features can be used.
To add a new feature to the feature vector either adjust the ElectionExperiment.py file or contact jita-mertlova.

Full example usage of this distance as the DAP distance, assuming 'myExperiment' is an experiment folder containing calculated
AgreementApprox, PolarizationApprox and DiversityApprox features.

experiment = mapof.prepare_offline_ordinal_experiment(experiment_id="myExperiment")
experiment.features["Agreement"] = experiment.import_feature("AgreementApprox")
experiment.features["Diversity"] = experiment.import_feature("DiversityApprox")
experiment.features["Polarization"] = experiment.import_feature("PolarizationApprox")
experiment.prepare_feature_vectors(['d', 'a', 'p'])
experiment.compute_distances(distance_id='feature_l2')
experiment.embed_2d(embedding_id='mds')
experiment.print_map_2d()
experiment.print_map_2d(legend=False)

"""


