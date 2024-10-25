import logging


def generate_real_identity_votes(num_voters=None, num_candidates=None):
    """ Generate real election that approximates identity (ID) """
    return [[j for j in range(num_candidates)] for _ in range(num_voters)]


def generate_real_antagonism_votes(num_voters=None, num_candidates=None):
    """ Generate real election that approximates antagonism (AN) """
    if num_voters % 2 != 0:
        logging.warning("Antagonism is not properly defined for odd number of voters")

    return [[j for j in range(num_candidates)] for _ in range(int(num_voters / 2))] + \
           [[num_candidates - j - 1 for j in range(num_candidates)] for _ in
            range(int(num_voters / 2))]
