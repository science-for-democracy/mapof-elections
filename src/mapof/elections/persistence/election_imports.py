import ast
import csv
import logging
import os
import re
from collections import Counter

import numpy as np

from mapof.elections.other.glossary import is_pseudo_culture

regex_file_name = r'# FILE NAME:'
regex_title = r'# TITLE:'
regex_data_type = r'# DATA TYPE:'
regex_number_alternatives = r"# NUMBER ALTERNATIVES:"
regex_number_voters = r"# NUMBER VOTERS:"
regex_number_unique_orders = r"# NUMBER UNIQUE ORDERS:"
regex_number_categories = r"# NUMBER CATEGORIES:"
regex_culture_id = r"# CULTURE ID:"
regex_params = r"# PARAMS:"


def import_distances(
        experiment_id: str,
        election_id: str,
        object_type: str = 'vote'
) -> np.ndarray:
    """
    Imports distances from a csv file.

    Parameters
    ----------
        experiment_id : str
            Name of the experiment.
        election_id : str
            Name of the election.
        object_type : str
            Object type.

    Returns
    -------
        np.ndarray
            Distances.
    """

    file_name = f'{election_id}_{object_type}.csv'
    path = os.path.join(os.getcwd(), 'experiments', experiment_id, 'distances',
                        file_name)

    with open(path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        length = int(len(list(reader)) ** 0.5)

    with open(path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        distances = np.zeros([length, length])
        for row in reader:
            distances[int(row['v1'])][int(row['v2'])] = float(row['distance'])
            distances[int(row['v2'])][int(row['v1'])] = float(row['distance'])

    return distances


def import_coordinates(
        experiment_id: str,
        election_id: str,
        object_type: str = 'vote'
) -> np.ndarray:
    """
    Imports coordinates from a csv file.

    Parameters
    ----------
        experiment_id : str
            Name of the experiment.
        election_id : str
            Name of the election.
        object_type : str
            Object type.

    Returns
    -------
        np.ndarray
            Distances.
    """

    file_name = f'{election_id}_{object_type}.csv'
    path = os.path.join(os.getcwd(), 'experiments', experiment_id, 'coordinates',
                        file_name)

    with open(path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        length = len(list(reader))

    with open(path, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file, delimiter=';')
        coordinates = np.zeros([length, 2])
        for row in reader:
            coordinates[int(row['vote_id'])] = [float(row['x']), float(row['y'])]

    return coordinates


def _process_fake_soc_line(line: str, matrix: list):
    row = [x.replace(" ", "") for x in line.split(',')]
    row = [float(x) for x in row]
    row = np.array(row)
    matrix.append(row)


def _process_soc_line(line: str, votes: list):
    tokens = line.split(':')
    nr_this_vote = int(tokens[0])
    vote = [int(x) for x in tokens[1].split(',')]
    vote = np.array(vote)
    for i in range(0, nr_this_vote):
        votes.append(vote)


def _process_app_line(line: str, votes: list):
    tokens = line.split(':')
    nr_this_vote = int(tokens[0])
    vote = set(eval(tokens[1]))
    for i in range(0, nr_this_vote):
        votes.append(vote)


def _process_soi_line(line: str, votes: list):
    pass


def _process_toc_line(line: str, votes: list):
    pass


def _process_toi_line(line: str, votes: list):
    pass


def import_real_new_soc_election(
        experiment_id: str = None,
        election_id: str = None,
        is_shifted=False,
        file_ending=4
):
    """ Import real ordinal election form .soc file """

    file_name = f'{election_id}.soc'
    path = os.path.join(os.getcwd(), "experiments", experiment_id, "elections", file_name)
    file = open(path, 'r')
    params = None
    culture_id = None
    votes = []
    num_candidates = 0
    nr_votes = 0
    nr_unique = 0
    alternative_names = list()
    from_file_file_name = ''
    from_file_title = ''
    from_file_data_type = ''
    # read metadata
    for line in file:
        if line[-1] == '\n':
            line = line[:-1]
        if line[0] != '#':
            if from_file_data_type == 'soc':
                _process_soc_line(line, votes)
            elif from_file_data_type == 'soi':
                _process_soi_line(line, votes)
            elif from_file_data_type == 'toc':
                _process_toc_line(line, votes)
            elif from_file_data_type == 'toi':
                _process_toi_line(line, votes)
            else:
                raise ValueError("Unknown data format.")
            break
        elif re.search(regex_file_name, line):
            from_file_file_name = line.split(':')[1][1:-file_ending]
        elif re.search(regex_title, line):
            from_file_title = line.split(':')[1].replace(" ", "")
        elif re.search(regex_data_type, line):
            from_file_data_type = line.split(':')[1].replace(" ", "")
        elif re.search(regex_number_alternatives, line):
            num_candidates = int(line.split(':')[1])
        elif re.search(regex_number_voters, line):
            num_voters = int(line.split(':')[1])
        elif re.search(regex_number_unique_orders, line):
            nr_unique = int(line.split(':')[1])
        elif re.search(regex_culture_id, line):
            culture_id = str(line.split(':')[1])
        elif re.search(regex_params, line):
            line = line.strip().split()
            if len(line) <= 2:
                params = {}
            else:
                params = ast.literal_eval(" ".join(line[2:]))

    if from_file_data_type == 'soc':
        for line in file:
            _process_soc_line(line, votes)
    elif from_file_data_type == 'soi':
        for line in file:
            _process_soi_line(line, votes)
    elif from_file_data_type == 'toc':
        for line in file:
            _process_toc_line(line, votes)
    elif from_file_data_type == 'toi':
        for line in file:
            _process_toi_line(line, votes)
    else:
        raise ValueError("Unknown data format.")

    file.close()

    alliances = None

    c = Counter(map(tuple, votes))
    counted_votes = [[count, list(row)] for row, count in c.items()]
    counted_votes = sorted(counted_votes, reverse=True)
    quantities = [a[0] for a in counted_votes]
    distinct_votes = [a[1] for a in counted_votes]
    num_options = len(counted_votes)

    if is_shifted:
        votes = [[vote - 1 for vote in voter] for voter in votes]

    return np.array(votes), \
           len(votes), \
           num_candidates, \
           params, \
           culture_id, \
           alliances, \
           num_options, \
           quantities, \
           distinct_votes


def import_real_old_soc_election(
        experiment_id: str = None,
        election_id: str = None,
        is_shifted=False
):
    """ Import real ordinal election form .soc file """
    logging.warning("Old soc format is no longer supported!")

    # file_name = f'{election_id}.soc'
    # path = os.path.join(os.getcwd(), "experiments", experiment_id, "elections", file_name)
    # my_file = open(path, 'r')
    #
    # params = 0
    # first_line = my_file.readline()
    #
    # if first_line[0] != '#':
    #     culture_id = 'empty'
    #     num_candidates = int(first_line)
    # else:
    #     first_line = first_line.strip().split()
    #     culture_id = first_line[1]
    #     if experiment_id == 'original_ordinal_map':
    #         params = {}
    #         culture_id = _old_name_extractor(first_line)
    #     else:
    #         if len(first_line) <= 2:
    #             params = {}
    #         else:
    #             params = ast.literal_eval(" ".join(first_line[2:]))
    #
    #     num_candidates = int(my_file.readline())
    #
    # alliances = {}
    # for i in range(num_candidates):
    #     line = my_file.readline().strip().split()
    #     if len(line) > 2:
    #         alliances[i] = int(line[2])
    #
    # line = my_file.readline().rstrip("\n").split(',')
    # num_voters = int(line[0])
    # num_options = int(line[2])
    # votes = [[0 for _ in range(num_candidates)] for _ in range(num_voters)]
    #
    # it = 0
    # quantities = []
    # for j in range(num_options):
    #     line = list(map(int, my_file.readline().rstrip("\n").split(',')))
    #     quantity = line[0]
    #     quantities.append(quantity)
    #
    #     for k in range(quantity):
    #         votes[it] = line[1:num_candidates + 1]
    #         it += 1
    #
    # c = Counter(map(tuple, votes))
    # counted_votes = [[count, list(row)] for row, count in c.items()]
    # counted_votes = sorted(counted_votes, reverse=True)
    # quantities = [a[0] for a in counted_votes]
    # distinct_votes = [a[1] for a in counted_votes]
    # num_options = len(counted_votes)
    #
    # if is_shifted:
    #     votes = [[vote - 1 for vote in voter] for voter in votes]
    # my_file.close()
    #
    # return np.array(votes), \
    #        num_voters, \
    #        num_candidates, \
    #        params, \
    #        culture_id, \
    #        alliances, \
    #        num_options, \
    #        quantities, \
    #        distinct_votes


def import_real_soc_election(**kwargs):
    try:
        return import_real_new_soc_election(**kwargs)
    except:
        return import_real_old_soc_election(**kwargs)


def import_pseudo_soc_election(*args):
    try:
        return import_pseudo_new_soc_election(*args)
    except:
        return import_pseudo_old_soc_election(*args)


def import_pseudo_new_soc_election(
        experiment_id: str,
        election_id: str,
):
    file_ending = 4
    file_name = f'{election_id}.soc'
    path = os.path.join(os.getcwd(), "experiments", experiment_id, "elections", file_name)
    file = open(path, 'r')
    params = None
    culture_id = None
    matrix = []
    num_candidates = 0
    nr_votes = 0
    nr_unique = 0
    alternative_names = list()
    from_file_file_name = ''
    from_file_title = ''
    from_file_data_type = ''
    # read metadata
    for line in file:
        if line[-1] == '\n':
            line = line[:-1]
        if line[0] != '#':
            if str(from_file_data_type) == 'soc':
                _process_fake_soc_line(line, matrix)
            else:
                raise ValueError("Unknown data format.")
            break
        elif re.search(regex_file_name, line):
            from_file_file_name = line.split(':')[1][1:-file_ending]
        elif re.search(regex_title, line):
            from_file_title = line.split(':')[1].replace(" ", "")
        elif re.search(regex_data_type, line):
            from_file_data_type = line.split(':')[1].replace(" ", "")
        elif re.search(regex_number_alternatives, line):
            num_candidates = int(line.split(':')[1])
        elif re.search(regex_number_voters, line):
            num_voters = int(line.split(':')[1])
        elif re.search(regex_number_unique_orders, line):
            nr_unique = int(line.split(':')[1])
        elif re.search(regex_culture_id, line):
            culture_id = str(line.split(':')[1]).replace(" ", "")
        elif re.search(regex_params, line):
            line = line.strip().split()
            if len(line) <= 2:
                params = {}
            else:
                params = ast.literal_eval(" ".join(line[2:]))

    if from_file_data_type == 'soc':
        for line in file:
            _process_fake_soc_line(line, matrix)
    else:
        raise ValueError("Unknown data format.")

    file.close()

    return culture_id, params, num_voters, num_candidates, matrix


def import_pseudo_old_soc_election(experiment_id: str, election_id: str):
    """ Import is_pseudo ordinal election form .soc file """

    print(f"Importing files in old format")

    file_name = f'{election_id}.soc'
    path = os.path.join(os.getcwd(), "experiments", experiment_id, "elections", file_name)
    my_file = open(path, 'r')

    first_line = my_file.readline()
    first_line = first_line.strip().split()
    culture_id = first_line[1]
    if len(first_line) <= 2:
        params = {}
    else:
        params = ast.literal_eval(" ".join(first_line[2:]))

    num_candidates = int(my_file.readline())
    num_voters = int(my_file.readline())

    my_file.close()

    return culture_id, params, num_voters, num_candidates, None


def import_real_new_app_election(
        experiment_id: str = None,
        election_id: str = None,
        is_shifted: bool = False,
        file_ending=4
):
    """ Import real approval election form .app file """

    file_name = f'{election_id}.app'
    path = os.path.join(os.getcwd(), "experiments", experiment_id, "elections", file_name)
    file = open(path, 'r')

    params = None
    culture_id = None
    votes = []
    num_candidates = 0
    nr_votes = 0
    nr_unique = 0
    alternative_names = list()
    from_file_file_name = ''
    from_file_title = ''
    from_file_data_type = ''
    # read metadata
    for line in file:
        if line[-1] == '\n':
            line = line[:-1]
        if line[0] != '#':
            if from_file_data_type == 'app':
                _process_app_line(line, votes)
            else:
                raise ValueError("Unknown data format.")
            break
        elif re.search(regex_file_name, line):
            from_file_file_name = line.split(':')[1][1:-file_ending]
        elif re.search(regex_title, line):
            from_file_title = line.split(':')[1].replace(" ", "")
        elif re.search(regex_data_type, line):
            from_file_data_type = line.split(':')[1].replace(" ", "")
        elif re.search(regex_number_alternatives, line):
            num_candidates = int(line.split(':')[1])
        elif re.search(regex_number_voters, line):
            num_voters = int(line.split(':')[1])
        elif re.search(regex_number_unique_orders, line):
            nr_unique = int(line.split(':')[1])
        elif re.search(regex_culture_id, line):
            culture_id = str(line.split(':')[1]).replace(" ", "")
        elif re.search(regex_params, line):
            line = line.strip().split()

            if len(line) <= 2:
                params = {}
            else:
                params = ast.literal_eval(" ".join(line[2:]))

    # label = from_file_title + "_" + from_file_file_name
    # read votes
    if from_file_data_type == 'app':
        for line in file:
            _process_app_line(line, votes)
    else:
        raise ValueError("Unknown data format.")

    file.close()

    c = Counter(map(tuple, votes))
    counted_votes = [[count, list(row)] for row, count in c.items()]
    counted_votes = sorted(counted_votes, reverse=True)
    quantities = [a[0] for a in counted_votes]
    distinct_votes = [a[1] for a in counted_votes]
    num_options = len(counted_votes)

    if is_shifted:
        votes = [[vote - 1 for vote in voter] for voter in votes]

    num_voters = len(votes)

    return votes, \
           num_voters, \
           num_candidates, \
           params, \
           culture_id, \
           num_options, \
           quantities, \
           distinct_votes


def import_real_old_app_election(
        experiment_id: str,
        election_id: str,
        is_shifted: bool = False
):
    """ Import real approval election from .app file """
    logging.warning("Old app format is no longer supported!")

    # file_name = f'{election_id}.app'
    # path = os.path.join(os.getcwd(), "experiments", experiment_id, "elections", file_name)
    # my_file = open(path, 'r')
    #
    # params = 0
    # first_line = my_file.readline()
    # if first_line[0] != '#':
    #     culture_id = 'empty'
    #     num_candidates = int(first_line)
    # else:
    #     first_line = first_line.strip().split()
    #     culture_id = first_line[1]
    #     if len(first_line) <= 2:
    #         params = {}
    #     else:
    #         params = ast.literal_eval(" ".join(first_line[2:]))
    #
    #     num_candidates = int(my_file.readline())
    #
    # for _ in range(num_candidates):
    #     my_file.readline()
    #
    # line = my_file.readline().rstrip("\n").split(',')
    # num_voters = int(line[0])
    # num_options = int(line[2])
    # votes = [set() for _ in range(num_voters)]
    #
    # it = 0
    # for j in range(num_options):
    #     line = my_file.readline().rstrip("\n").replace("{", ''). \
    #         replace("}", '').replace(' ', '').split(',')
    #     if line[1] != '':
    #         quantity = int(line[0])
    #         for k in range(quantity):
    #             for el in range(len(line) - 1):
    #                 votes[it].add(int(line[el + 1]))
    #             it += 1
    #
    # # if culture_id in NICE_NAME.values():
    # #     rev_dict = dict(zip(NICE_NAME.values(), NICE_NAME.keys()))
    # #     culture_id = rev_dict[culture_id]
    #
    # if is_shifted:
    #     votes = [{c - 1 for c in vote} for vote in votes]
    # my_file.close()
    #
    # c = Counter(map(tuple, votes))
    # counted_votes = [[count, list(row)] for row, count in c.items()]
    # counted_votes = sorted(counted_votes, reverse=True)
    # quantities = [a[0] for a in counted_votes]
    # distinct_votes = [a[1] for a in counted_votes]
    # num_options = len(counted_votes)
    #
    # return votes, \
    #        num_voters, \
    #        num_candidates, \
    #        params, \
    #        culture_id, \
    #        num_options, \
    #        quantities, \
    #        distinct_votes


def import_real_app_election(**kwargs):
    try:
        return import_real_new_app_election(**kwargs)
    except:
        return import_real_old_app_election(**kwargs)


def check_if_pseudo(experiment_id, election_id):
    file_ending = 4
    file_name = f'{election_id}.soc'
    path = os.path.join(os.getcwd(), "experiments", experiment_id, "elections", file_name)
    file = open(path, 'r')
    params = None
    culture_id = None
    matrix = []
    num_candidates = 0
    nr_votes = 0
    nr_unique = 0
    alternative_names = list()
    from_file_file_name = ''
    from_file_title = ''
    from_file_data_type = ''
    # read metadata
    for line in file:
        if line[-1] == '\n':
            line = line[:-1]
        if line[0] != '#':
            if from_file_data_type == 'soc':
                _process_fake_soc_line(line, matrix)
            else:
                raise ValueError("Unknown data format.")
            break
        elif re.search(regex_file_name, line):
            from_file_file_name = line.split(':')[1][1:-file_ending]
        elif re.search(regex_title, line):
            from_file_title = line.split(':')[1].replace(" ", "")
        elif re.search(regex_data_type, line):
            from_file_data_type = line.split(':')[1].replace(" ", "")
        elif re.search(regex_number_alternatives, line):
            num_candidates = int(line.split(':')[1])
        elif re.search(regex_number_voters, line):
            num_voters = int(line.split(':')[1])
        elif re.search(regex_number_unique_orders, line):
            nr_unique = int(line.split(':')[1])
        elif re.search(regex_culture_id, line):
            culture_id = str(line.split(':')[1]).replace(" ", "")
            break
        elif re.search(regex_params, line):
            line = line.strip().split()
            if len(line) <= 2:
                params = {}
            else:
                params = ast.literal_eval(" ".join(line[2:]))
    return is_pseudo_culture(str(culture_id))


# def _old_name_extractor(first_line: str) -> str:
#     if len(first_line) == 4:
#         culture_id = f'{first_line[1]} {first_line[2]} {first_line[3]}'
#     elif len(first_line) == 3:
#         culture_id = f'{first_line[1]} {first_line[2]}'
#     elif len(first_line) == 2:
#         culture_id = first_line[1]
#     else:
#         culture_id = 'noname'
#     return culture_id
