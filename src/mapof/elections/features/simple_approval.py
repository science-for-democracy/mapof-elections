

import numpy as np
import scipy.special
import math


def justified_ratio(election, feature_params) -> dict:
    # 1-large, 1-cohesive
    election.compute_reverse_approvals()
    threshold = election.num_voters / feature_params['committee_size']
    covered = set()
    for _set in election.reverse_approvals:
        if len(_set) >= threshold:
            covered = covered.union(_set)
    print(len(covered) / float(election.num_voters))
    return {'value': len(covered) / float(election.num_voters)}


def abstract(election) -> dict:
    n = election.num_voters
    election.votes_to_approvalwise_vector()
    vector = election.approvalwise_vector
    total_value = 0
    for i in range(election.num_candidates):
        k = vector[i] * n
        x = scipy.special.binom(n, k)
        x = math.log(x)
        total_value += x
    return {'value': total_value}


def max_approval_score(election):
    """
    Computes the largest approval score of a given election.

    Parameters
    ----------
        election : ApprovalElection

    Returns
    -------
        dict
            'value': max approval score
    """
    score = np.zeros([election.num_candidates])
    for vote in election.votes:
        for c in vote:
            score[c] += 1
    return {'value': max(score)}