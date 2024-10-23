import numpy as np


def num_of_diff_votes(election):
    if election.fake:
        return {'value': None}

    str_votes = [str(vote) for vote in election.votes]
    return {'value': len(set(str_votes))}


def borda_diversity(election):
    if election.fake:
        return {'value': None}

    vector = np.array(election.get_bordawise_vector())
    return {'value': np.std(vector)}
