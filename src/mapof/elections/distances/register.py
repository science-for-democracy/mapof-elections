
registered_ordinal_election_distances = {}

registered_approval_election_distances = {}


def register_ordinal_election_distance(feature_id: str):

    def decorator(func):
        registered_ordinal_election_distances[feature_id] = func
        return func

    return decorator


def register_approval_election_distance(feature_id: str):

    def decorator(func):
        registered_approval_election_distances[feature_id] = func
        return func

    return decorator
