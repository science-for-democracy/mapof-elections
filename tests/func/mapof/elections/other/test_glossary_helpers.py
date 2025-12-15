from mapof.elections.other.glossary import is_pseudo_culture


def test_is_pseudo_culture_recognizes_known_models():
    assert is_pseudo_culture('pseudo_uniformity')
    assert is_pseudo_culture('pseudo_custom_model')


def test_is_pseudo_culture_handles_non_pseudo_and_none():
    assert not is_pseudo_culture('impartial')
    assert not is_pseudo_culture(None)
