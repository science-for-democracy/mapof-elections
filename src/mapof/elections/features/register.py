

registered_simple_ordinal_features = {
}


def register_simple_ordinal_feature(feature_id: str):

    def decorator(func):
        registered_simple_ordinal_features[feature_id] = func
        return func

    return decorator

