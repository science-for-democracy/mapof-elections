#!/usr/bin/env python

import csv
import os

from mapof.elections.cultures import registered_pseudo_ordinal_cultures
from mapof.elections.objects.OrdinalElectionExperiment import OrdinalElectionExperiment


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


def generate_frequency_matrix(
        culture_id=None,
        num_candidates=None,
        params=None):

    return registered_pseudo_ordinal_cultures[culture_id](
        num_candidates=num_candidates,
        params=params
    )
