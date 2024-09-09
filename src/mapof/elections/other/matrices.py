#!/usr/bin/env python

from mapof.elections.cultures.matrices.group_separable_matrices import get_gs_caterpillar_vectors
from mapof.elections.cultures.matrices.single_peaked_matrices import get_walsh_vectors, \
    get_conitzer_vectors
from mapof.elections.cultures.matrices.single_crossing_matrices import get_single_crossing_vectors

from mapof.elections.objects.Election import Election
from mapof.elections.objects.OrdinalElectionExperiment import OrdinalElectionExperiment

from mapof.elections.cultures.mallows import get_mallows_matrix

import os
import csv


def prepare_matrices(experiment_id):
    """ compute positionwise matrices and
    is_exported them in the /matrices folder """
    experiment = OrdinalElectionExperiment(experiment_id)

    path = os.path.join(os.getcwd(), "experiment", experiment_id, "matrices")
    for file_name in os.listdir(path):
        os.remove(os.path.join(path, file_name))

    for election_id in experiment.elections:
        matrix = experiment.elections[election_id].votes_to_positionwise_matrix()
        file_name = election_id + ".csv"
        path = os.path.join(os.getcwd(), "experiment", experiment_id,
                            "matrices", file_name)

        with open(path, 'w', newline='') as csv_file:

            writer = csv.writer(csv_file, delimiter=';')
            header = [str(i) for i in range(experiment.elections[election_id].num_candidates)]
            writer.writerow(header)
            for row in matrix:
                writer.writerow(row)


def generate_positionwise_matrix(model_id=None, num_candidates=None,
                                 num_voters=100, params=None):

    if model_id == 'conitzer_matrix':
        vectors = get_conitzer_vectors(num_candidates)
    elif model_id == 'walsh_matrix':
        vectors = get_walsh_vectors(num_candidates)
    elif model_id == 'single-crossing_matrix':
        vectors = get_single_crossing_vectors(num_candidates)
    elif model_id == 'gs_caterpillar_matrix':
        vectors = get_gs_caterpillar_vectors(num_candidates)
    elif model_id == 'norm-mallows_matrix':
        return get_mallows_matrix(num_candidates, params)

    return vectors.transpose()


def get_positionwise_matrix(votes):
    election = Election("virtual", "virtual", votes=votes)
    return election.votes_to_positionwise_matrix()
