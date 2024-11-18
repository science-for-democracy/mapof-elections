import csv
import os
from collections import Counter

from mapof.core.utils import make_folder_if_do_not_exist


def export_votes_to_file(
        election,
        path,
        votes=None,
        is_aggregated=True
) -> None:
    """
    Exports votes to a file.

    Parameters
    ----------
        election
            Election.
        path:
            Path to the place in which the file should be stored.
        votes:
            Votes.
        is_aggregated : bool
            If True then votes are stored in aggregated way.

    Returns
    -------
        None
    """

    if votes is None:
        votes = election.votes

    with open(path, 'w') as file_:
        file_.write(f'# FILE NAME: {election.election_id}.{election.format}\n')
        file_.write(f'# DATA TYPE: {election.format} \n')
        file_.write(f'# CULTURE ID: {election.culture_id} \n')
        file_.write(f'# PARAMS: {str(election.params)} \n')
        file_.write(f'# NUMBER ALTERNATIVES: {election.num_candidates} \n')
        file_.write(f'# NUMBER VOTERS: {election.num_voters} \n')

        if is_aggregated:

            c = Counter(map(tuple, votes))
            counted_votes = [[count, list(row)] for row, count in c.items()]
            counted_votes = sorted(counted_votes, reverse=True)

            if election.instance_type == 'approval':
                for i in range(len(counted_votes)):
                    file_.write(str(counted_votes[i][0]) + ': {')
                    for j in range(len(counted_votes[i][1])):
                        file_.write(str(int(counted_votes[i][1][j])))
                        if j < len(counted_votes[i][1]) - 1:
                            file_.write(", ")
                    file_.write("}\n")

            elif election.instance_type == 'ordinal':
                for i in range(len(counted_votes)):
                    file_.write(str(counted_votes[i][0]) + ': ')
                    for j in range(len(counted_votes[i][1])):
                        file_.write(str(int(counted_votes[i][1][j])))
                        if j < len(counted_votes[i][1]) - 1:
                            file_.write(", ")
                    file_.write("\n")
        else:

            if election.instance_type == 'approval':
                for i in range(len(votes)):
                    file_.write('1: {')
                    for j in range(len(votes[i])):
                        file_.write(str(int(list(votes[i])[j])))
                        if j < len(votes[i]) - 1:
                            file_.write(", ")
                    file_.write("}\n")

            elif election.instance_type == 'ordinal':
                for i in range(len(votes)):
                    file_.write('1: ')
                    for j in range(len(votes[i])):
                        file_.write(str(int(votes[i][j])))
                        if j < len(votes[i]) - 1:
                            file_.write(", ")
                    file_.write("\n")



def export_election_without_experiment(
        election,
        path_to_folder,
        is_aggregated: bool = True
) -> None:
    """
    Exports election in an .app file

    Parameters
    ----------
        election
            Election.
        path_to_folder
            Path to a folder to which the election should be exported.
        is_aggregated : bool
            If True then votes are stored in aggregated way.

    Returns
    -------
        None
    """

    path_to_file = os.path.join(path_to_folder, f'{election.election_id}.{election.format}')

    if election.is_pseudo:
        export_pseudo_ordinal_election(election, path_to_file)
    else:
        export_votes_to_file(election,
                             path_to_file,
                             votes=election.votes,
                             is_aggregated=is_aggregated)


def export_election_within_experiment(
        election,
        is_aggregated: bool = True
) -> None:
    """
    Exports election in an .app file

    Parameters
    ----------
        election
            Election.
        is_aggregated : bool
            If True then votes are stored in aggregated way.

    Returns
    -------
        None
    """
    path_to_folder = os.path.join(os.getcwd(), "experiments", election.experiment_id, "elections")
    make_folder_if_do_not_exist(path_to_folder)

    path_to_file = os.path.join(path_to_folder, f'{election.election_id}.{election.format}')

    if election.is_pseudo:
        export_pseudo_ordinal_election(election, path_to_file)
    else:
        export_votes_to_file(election,
                             path_to_file,
                             votes=election.votes,
                             is_aggregated=is_aggregated)


def export_pseudo_ordinal_election(election, path):

    file_ = open(path, 'w')
    file_.write(f'# FILE NAME: {election.election_id}.{election.format}\n')
    file_.write(f'# DATA TYPE: soc \n')
    file_.write(f'# CULTURE ID: {election.culture_id} \n')
    file_.write(f'# PARAMS: {str(election.params)} \n')
    file_.write(f'# NUMBER ALTERNATIVES: {election.num_candidates} \n')
    file_.write(f'# NUMBER VOTERS: {election.num_voters} \n')

    frequency_matrix = election.get_frequency_matrix()

    for i in range(election.num_candidates):
        for j in range(election.num_candidates):
            file_.write(str(frequency_matrix[i][j]))
            if j < election.num_candidates - 1:
                file_.write(", ")
        file_.write("\n")

    file_.close()


#
# def export_ordinal_election_without_experiment(
#         path_to_folder,
#         election,
#         is_aggregated: bool = True
# ) -> None:
#     """
#     Exports ordinal election to a .soc file
#
#     Parameters
#     ----------
#         path_to_folder
#             Path to a folder to which the election should be exported.
#         election
#             Ordinal Election.
#         is_aggregated : bool
#             If True then votes are stored in aggregated way.
#
#     Returns
#     -------
#         None
#     """
#
#     path_to_file = os.path.join(path_to_folder, f'{election.election_id}.soc')
#
#     if election.is_pseudo:
#         export_pseudo_ordinal_election(election, path_to_file)
#     else:
#         export_votes_to_file(election,
#                              path_to_file,
#                              instance_type='ordinal',
#                              votes=election.votes,
#                              is_aggregated=is_aggregated)
#
#
# def export_ordinal_election_with_experiment(
#         election,
#         is_aggregated: bool = True
# ) -> None:
#     """
#     Exports ordinal election to a .soc file
#
#     Parameters
#     ----------
#         election
#             Ordinal Election.
#         is_aggregated : bool
#             If True then votes are stored in aggregated way.
#
#     Returns
#     -------
#         None
#     """
#
#     path_to_folder = os.path.join(os.getcwd(), "experiments", election.experiment_id, "elections")
#     make_folder_if_do_not_exist(path_to_folder)
#     path_to_file = os.path.join(path_to_folder, f'{election.election_id}.soc')
#
#     if election.is_pseudo:
#         export_pseudo_ordinal_election(election, path_to_file)
#     else:
#         export_votes_to_file(election,
#                              election.culture_id,
#                              election.num_candidates,
#                              election.num_voters,
#                              election.params,
#                              path_to_file,
#                              instance_type='ordinal',
#                              votes=election.votes,
#                              is_aggregated=is_aggregated)


def export_distances(
        election,
        object_type: str = 'vote'
) -> None:
    """
    Exports distances to a csv file.

    Parameters
    ----------
        election
            Election.
        object_type : str
            Object type.

    Returns
    -------
        None
    """

    file_name = f'{election.election_id}_{object_type}.csv'
    path = os.path.join(os.getcwd(), "experiments", election.experiment_id, "distances",
                        file_name)
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["v1", "v2", "distance"])
        for v1 in range(len(election.distances[object_type])):
            for v2 in range(len(election.distances[object_type])):
                distance = str(election.distances[object_type][v1][v2])
                writer.writerow([v1, v2, distance])


def export_coordinates(
        election,
        object_type: str = 'vote'
) -> None:
    """
    Exports coordinates to a csv file.

    Parameters
    ----------
        election
            Election
        object_type : str
            Object type.

    Returns
    -------
        None
    """

    file_name = f'{election.election_id}_{object_type}.csv'
    path = os.path.join(os.getcwd(), "experiments", election.experiment_id, "coordinates",
                        file_name)
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["vote_id", "x", "y"])
        for vote_id in range(len(election.coordinates[object_type])):
            x = str(election.coordinates[object_type][vote_id][0])
            y = str(election.coordinates[object_type][vote_id][1])
            writer.writerow([vote_id, x, y])


def export_frequency_matrices(experiment) -> None:
    """ Exports frequency matrices to csv files.

    Parameters
    ----------
        experiment
            Experiment.

    Returns
    -------
        None
    """

    path_to_folder = os.path.join(os.getcwd(), "experiments", experiment.experiment_id, "matrices")

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)

    for file_name in os.listdir(path_to_folder):
        os.remove(os.path.join(path_to_folder, file_name))

    for election_id in experiment.elections:
        frequency_matrix = experiment.elections[election_id].get_frequency_matrix()
        file_name = election_id + ".csv"

        path_to_file = os.path.join(path_to_folder, file_name)
        with open(path_to_file, 'w', newline='') as csv_file:

            writer = csv.writer(csv_file, delimiter=';')
            for row in frequency_matrix:
                writer.writerow(row)
