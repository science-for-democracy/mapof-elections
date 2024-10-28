import numpy as np

from mapof.elections.features.register import register_ordinal_election_feature


@register_ordinal_election_feature('num_of_diff_votes')
def num_of_diff_votes(election):
    if election.is_pseudo:
        return {'value': None}

    str_votes = [str(vote) for vote in election.votes]
    return {'value': len(set(str_votes))}


@register_ordinal_election_feature('borda_diversity')
def borda_diversity(election):
    if election.is_pseudo:
        return {'value': None}

    vector = np.array(election.get_bordawise_vector())
    return {'value': np.std(vector)}
