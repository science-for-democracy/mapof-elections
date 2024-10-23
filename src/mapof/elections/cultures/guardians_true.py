import numpy as np

from prefsampling.ordinal import impartial as generate_ordinal_ic_votes


def generate_real_identity_votes(num_voters=None, num_candidates=None):
    """ Generate real election that approximates identity (ID) """
    return [[j for j in range(num_candidates)] for _ in range(num_voters)]


def generate_real_antagonism_votes(num_voters=None, num_candidates=None):
    """ Generate real election that approximates antagonism (AN) """
    return [[j for j in range(num_candidates)] for _ in range(int(num_voters / 2))] + \
           [[num_candidates - j - 1 for j in range(num_candidates)] for _ in
            range(int(num_voters / 2))]

