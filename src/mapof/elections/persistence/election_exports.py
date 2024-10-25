import csv
from collections import Counter

from mapof.core.utils import *

from mapof.elections.other.glossary import APPROVAL_FAKE_MODELS


def export_votes_to_file(
        election,
        culture_id: str,
        num_candidates: int,
        num_voters: int,
        params: dict,
        path,
        ballot_type,
        votes=None,
        is_aggregated=True
) -> None:
    """
    Exports votes to a file.

    Parameters
    ----------
        election
            Election.
        culture_id: str
            Culture id.
        num_candidates : int
            Number of Candidates
        num_voters : int
            Number of Voters
        params : int
            Model params to be exported.
        path:
            Path to the place in which the file should be stored.
        ballot_type:
            Ballot type.
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

    if params is None:
        params = {}

    with open(path, 'w') as file_:
        if ballot_type == 'ordinal':
            file_.write(f'# FILE NAME: {election.election_id}.soc\n')
            file_.write(f'# DATA TYPE: soc \n')
        elif ballot_type == 'approval':
            file_.write(f'# FILE NAME: {election.election_id}.app\n')
            file_.write(f'# DATA TYPE: app \n')
        file_.write(f'# CULTURE ID: {culture_id} \n')
        file_.write(f'# PARAMS: {str(params)} \n')
        file_.write(f'# NUMBER ALTERNATIVES: {num_candidates} \n')
        file_.write(f'# NUMBER VOTERS: {num_voters} \n')

        if is_aggregated:

            c = Counter(map(tuple, votes))
            counted_votes = [[count, list(row)] for row, count in c.items()]
            counted_votes = sorted(counted_votes, reverse=True)

            if ballot_type == 'approval':
                for i in range(len(counted_votes)):
                    file_.write(str(counted_votes[i][0]) + ': {')
                    for j in range(len(counted_votes[i][1])):
                        file_.write(str(int(counted_votes[i][1][j])))
                        if j < len(counted_votes[i][1]) - 1:
                            file_.write(", ")
                    file_.write("}\n")

            elif ballot_type == 'ordinal':
                for i in range(len(counted_votes)):
                    file_.write(str(counted_votes[i][0]) + ': ')
                    for j in range(len(counted_votes[i][1])):
                        file_.write(str(int(counted_votes[i][1][j])))
                        if j < len(counted_votes[i][1]) - 1:
                            file_.write(", ")
                    file_.write("\n")
        else:

            # file_.write(str(num_voters) + ', ' + str(num_voters) + ', ' +
            #             str(num_voters) + "\n")

            if ballot_type == 'approval':
                for i in range(len(votes)):
                    file_.write('1: {')
                    for j in range(len(votes[i])):
                        file_.write(str(int(list(votes[i])[j])))
                        if j < len(votes[i]) - 1:
                            file_.write(", ")
                    file_.write("}\n")

            elif ballot_type == 'ordinal':
                for i in range(len(votes)):
                    file_.write('1: ')
                    for j in range(len(votes[i])):
                        file_.write(str(int(votes[i][j])))
                        if j < len(votes[i]) - 1:
                            file_.write(", ")
                    file_.write("\n")


def export_approval_election(
        election,
        is_aggregated: bool = True
):
    """
    Exports approval election in an .app file

    Parameters
    ----------
        election
            Election.
        is_aggregated : bool
            If True then votes are stored in aggregated way.
    """
    path_to_folder = os.path.join(os.getcwd(), "experiments", election.experiment_id, "elections")
    make_folder_if_do_not_exist(path_to_folder)
    path_to_file = os.path.join(path_to_folder, f'{election.election_id}.app')

    if election.culture_id in APPROVAL_FAKE_MODELS:
        file_ = open(path_to_file, 'w')
        file_.write(f'$ {election.culture_id} {election.params} \n')
        file_.write(str(election.num_candidates) + '\n')
        file_.write(str(election.num_voters) + '\n')
        file_.close()

    else:
        export_votes_to_file(election,
                             election.culture_id,
                             election.num_candidates,
                             election.num_voters,
                             election.params,
                             path_to_file,
                             ballot_type='approval',
                             votes=election.votes,
                             is_aggregated=is_aggregated)


def export_pseudo_ordinal_election(election, path_to_file):
    file_ = open(path_to_file, 'w')
    file_.write(f'# FILE NAME: {election.election_id}.soc\n')
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


def export_ordinal_election(
        election,
        is_aggregated: bool = True
):
    """
    Exports ordinal election to a .soc file

    Parameters
    ----------
        election
            Election.
        is_aggregated : bool
            If True then votes are stored in aggregated way.
    """

    path_to_folder = os.path.join(os.getcwd(), "experiments", election.experiment_id, "elections")
    make_folder_if_do_not_exist(path_to_folder)
    path_to_file = os.path.join(path_to_folder, f'{election.election_id}.soc')

    if election.is_pseudo:
        export_pseudo_ordinal_election(election, path_to_file)
    else:
        export_votes_to_file(election,
                             election.culture_id,
                             election.num_candidates,
                             election.num_voters,
                             election.params,
                             path_to_file,
                             ballot_type='ordinal',
                             votes=election.votes,
                             is_aggregated=is_aggregated)


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


def export_frequency_matrices(exp) -> None:
    """ Exports frequency matrices to csv files. """

    path_to_folder = os.path.join(os.getcwd(), "experiments", exp.experiment_id, "matrices")

    if not os.path.exists(path_to_folder):
        os.makedirs(path_to_folder)

    for file_name in os.listdir(path_to_folder):
        os.remove(os.path.join(path_to_folder, file_name))

    for election_id in exp.elections:
        frequency_matrix = exp.elections[election_id].get_frequency_matrix()
        file_name = election_id + ".csv"

        path_to_file = os.path.join(path_to_folder, file_name)
        with open(path_to_file, 'w', newline='') as csv_file:

            writer = csv.writer(csv_file, delimiter=';')
            for row in frequency_matrix:
                writer.writerow(row)