#!/usr/bin/env python
# UNDER CONSTRUCTION #

import os
import random as rand
from collections import Counter

import numpy as np
from scipy.stats import gamma

from mapel.voting.glossary import LIST_OF_PREFLIB_MODELS


# MATRICES
def get_sushi_vectors():
    return np.array(get_sushi_matrix()).transpose()


def get_sushi_matrix():
    return [[0.11, 0.0808, 0.0456, 0.1494, 0.109, 0.0412, 0.3426, 0.0226, 0.0072, 0.0916],
            [0.1058, 0.1546, 0.0644, 0.1302, 0.1304, 0.0358, 0.2056, 0.051, 0.0132, 0.109],
            [0.1138, 0.1594, 0.0884, 0.096, 0.1266, 0.0548, 0.1276, 0.0874, 0.0246, 0.1214],
            [0.109, 0.1474, 0.1048, 0.0754, 0.1182, 0.068, 0.0862, 0.1168, 0.034, 0.1402],
            [0.1004, 0.1376, 0.129, 0.061, 0.0924, 0.0888, 0.0666, 0.1394, 0.047, 0.1378],
            [0.1042, 0.116, 0.1348, 0.0632, 0.0846, 0.0954, 0.048, 0.1528, 0.0804, 0.1206],
            [0.097, 0.0832, 0.1324, 0.0568, 0.079, 0.1306, 0.0422, 0.1682, 0.1094, 0.1012],
            [0.0982, 0.0636, 0.1214, 0.0638, 0.0728, 0.1546, 0.0376, 0.1396, 0.166, 0.0824],
            [0.0836, 0.0352, 0.1048, 0.1084, 0.101, 0.1692, 0.0236, 0.0958, 0.2222, 0.0562],
            [0.078, 0.0222, 0.0744, 0.1958, 0.086, 0.1616, 0.02, 0.0264, 0.296, 0.0396]]


# GENERATE
def generate_elections_preflib(experiment_id, election_model=None, elections_id=None,
                               num_voters=None, num_candidates=None, special=None, folder=None,
                               selection_method='random'):
    """ main function: generate elections"""

    votes = generate_votes_preflib(election_model, selection_method=selection_method,
                                   num_voters=num_voters, num_candidates=num_candidates, folder=folder)

    path = os.path.join("experiments", experiment_id, "elections", elections_id + ".soc")
    file_ = open(path, 'w')

    file_.write(str(num_candidates) + "\n")

    for i in range(num_candidates):
        file_.write(str(i) + ', c' + str(i) + "\n")

    c = Counter(map(tuple, votes))
    counted_votes = [[count, list(row)] for row, count in c.items()]
    counted_votes = sorted(counted_votes, reverse=True)

    file_.write(str(num_voters) + ', ' + str(num_voters) + ', ' + str(len(counted_votes)) + "\n")

    for i in range(len(counted_votes)):
        file_.write(str(counted_votes[i][0]) + ', ')
        for j in range(num_candidates):
            file_.write(str(counted_votes[i][1][j]))
            if j < num_candidates - 1:
                file_.write(", ")
            else:
                file_.write("\n")

    file_.close()


# REAL
def generate_votes_preflib(elections_model, num_voters=None, num_candidates=None, folder=None,
                           selection_method=None):
    """ Generate votes based on elections from Preflib """

    long_name = str(elections_model)
    file_name = 'real_data/' + folder + '/' + long_name + '.txt'
    file_votes = open(file_name, 'r')
    original_num_voters = int(file_votes.readline())
    if original_num_voters == 0:
        return [0, 0, 0]
    original_num_candidates = int(file_votes.readline())
    choice = [x for x in range(original_num_voters)]
    rand.shuffle(choice)

    votes = np.zeros([num_voters, original_num_candidates], dtype=int)
    original_votes = np.zeros([original_num_voters, original_num_candidates], dtype=int)

    for j in range(original_num_voters):
        value = file_votes.readline().strip().split(',')
        for k in range(original_num_candidates):
            original_votes[j][k] = int(value[k])

    file_votes.close()

    for j in range(num_voters):
        r = rand.randint(0, original_num_voters - 1)
        for k in range(original_num_candidates):
            votes[j][k] = original_votes[r][k]

    for i in range(num_voters):
        if len(votes[i]) != len(set(votes[i])):
            print('wrong data')

    # REMOVE SURPLUS CANDIDATES
    if num_candidates < original_num_candidates:
        new_votes = []

        # NEW 17.12.2020
        if selection_method == 'random':
            selected_candidates = rand.sample([j for j in range(original_num_candidates)], num_candidates)
        elif selection_method == 'borda':
            scores = get_borda_scores(original_votes, original_num_voters, original_num_candidates)
            order_by_score = [x for _, x in
                              sorted(zip(scores, [i for i in range(original_num_candidates)]), reverse=True)]
            selected_candidates = order_by_score[0:num_candidates]
        elif selection_method == 'freq':
            freq = import_freq(elections_model)
            # print(freq)
            selected_candidates = freq[0:num_candidates]
        else:
            raise NameError('No such selection method!')

        mapping = {}
        for j in range(num_candidates):
            mapping[str(selected_candidates[j])] = j
        for j in range(num_voters):
            vote = []
            for k in range(original_num_candidates):
                cand = votes[j][k]
                if cand in selected_candidates:
                    vote.append(mapping[str(cand)])
            if len(vote) != len(set(vote)):
                print(vote)
            new_votes.append(vote)
        return new_votes
    else:
        return votes


def import_freq(elections_model):
    path = 'real_data/freq/' + elections_model + '.txt'
    with open(path, 'r', newline='') as txt_file:
        line = txt_file.readline().strip().split(',')
        line = line[0:len(line) - 1]
        for i in range(len(line)):
            line[i] = int(line[i])
    return line


def get_borda_scores(votes, num_voters, num_candidates):
    scores = [0 for _ in range(num_candidates)]
    for i in range(num_voters):
        for j in range(num_candidates):
            scores[votes[i][j]] += num_candidates - j - 1

    return scores