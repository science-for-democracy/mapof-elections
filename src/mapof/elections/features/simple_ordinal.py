import logging
import math

from mapof.elections.features.register import register_ordinal_election_feature


@register_ordinal_election_feature('is_condorcet')
def is_condorcet(election) -> dict:
    """
    Checks if election witness Condorcet winner

    Parameters
    ----------
        election : OrdinalElection

    Returns
    -------
        dict
            'value': True if Condorcet winner exists, False otherwise
    """
    if election.is_pseudo:
        return {'value': None}

    potes = election.get_potes()  # get positional votes
    for i in range(election.num_candidates):

        condocret_winner = True
        for j in range(election.num_candidates):

            diff = 0
            for k in range(election.num_voters):

                if potes[k][i] <= potes[k][j]:
                    diff += 1

            if diff < math.ceil((election.num_voters + 1) / 2.):
                condocret_winner = False
                break

        if condocret_winner:
            return {'value': True}

    return {'value': False}


@register_ordinal_election_feature('effective_num_candidates')
def get_effective_num_candidates(election, mode='Borda') -> dict:
    """ Compute effective number of candidates of a given election."""
    if election.is_pseudo:
        return {'value': None}

    c = election.num_candidates
    matrix = election.get_frequency_matrix()

    if mode == 'Borda':
        all_scores = [sum([matrix[j][i] * (c - i - 1) for i in range(c)]) / (c * (c - 1) / 2)
                      for j in range(c)]
    elif mode == 'Plurality':
        all_scores = [sum([matrix[j][i] for i in range(1)]) for j in range(c)]
    else:
        logging.warning(f"Mode {mode} is not supported.")
        all_scores = []

    return {'value': 1. / sum([x * x for x in all_scores])}
