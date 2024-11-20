import logging


from mapof.elections.objects.ApprovalElection import ApprovalElection
from mapof.elections.distances.register import register_approval_election_distance


@register_approval_election_distance("approvalwise")
def approvalwise_distance(
        election_1: ApprovalElection,
        election_2: ApprovalElection,
        inner_distance: callable
) -> (float, list):
    """ Return: approvalwise distance """
    election_1.votes_to_approvalwise_vector()
    election_2.votes_to_approvalwise_vector()
    return inner_distance(election_1.approvalwise_vector, election_2.approvalwise_vector), None


@register_approval_election_distance("hamming")
def hamming_distance(election_1: ApprovalElection, election_2: ApprovalElection) -> float:
    """ Return: Hamming distance """
    logging.warning("Hamming distance is not implemented yet.")
    return -1

