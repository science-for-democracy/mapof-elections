import numpy as np
from mapof.elections.persistence.election_imports import (
    import_distances,
    import_coordinates,
    import_ordinal_election,
    import_pseudo_ordinal_election,
    import_approval_election,
    check_if_pseudo,
)


def test_import_distances(mocker):
    csv = """v1;v2;distance
0;0;0.0
0;1;1.0
1;0;1.0
1;1;0.0
"""
    mocked_open = mocker.mock_open(read_data=csv)
    mocker.patch("builtins.open", mocked_open)

    arr = import_distances("experimentX", "electionX", object_type='vote')
    expected = np.array([[0.0, 1.0], [1.0, 0.0]])
    assert np.allclose(arr, expected)


def test_import_coordinates(mocker):
    csv = """vote_id;x;y
0;1.0;2.0
1;3.0;4.0
"""
    mocked_open = mocker.mock_open(read_data=csv)
    mocker.patch("builtins.open", mocked_open)

    coords = import_coordinates("experimentX", "electionX", object_type='vote')
    expected = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert np.allclose(coords, expected)


def test_import_ordinal_election_soc(mocker):
    soc = """# FILE NAME: example.soc
# TITLE: Example
# DATA TYPE: soc
# NUMBER ALTERNATIVES: 3
# NUMBER VOTERS: 1
# NUMBER UNIQUE ORDERS: 1
# CULTURE ID: culture_x
# PARAMS:
1:1,2,3
"""
    mocked_open = mocker.mock_open(read_data=soc)
    mocker.patch("builtins.open", mocked_open)

    votes, nr_votes, num_candidates, params, culture_id, alliances, num_distinct_votes, quantities, distinct_votes = import_ordinal_election(
        experiment_id="exp", election_id="example"
    )

    assert nr_votes == 1
    assert num_candidates == 3
    assert culture_id == ' culture_x' or culture_id == 'culture_x'
    assert num_distinct_votes == 1
    assert quantities == [1]
    assert distinct_votes == [[1, 2, 3]]
    # votes returned as numpy array of arrays
    assert votes.shape[0] == 1


def test_import_pseudo_ordinal_election(mocker):
    soc = """# FILE NAME: example.soc
# TITLE: Example
# DATA TYPE: soc
# NUMBER ALTERNATIVES: 3
# NUMBER VOTERS: 1
# NUMBER UNIQUE ORDERS: 1
# CULTURE ID: pseudo_uniformity
# PARAMS:
0.1,0.2,0.7
"""
    mocked_open = mocker.mock_open(read_data=soc)
    mocker.patch("builtins.open", mocked_open)

    culture_id, params, num_voters, num_candidates, matrix = import_pseudo_ordinal_election(
        experiment_id="exp", election_id="example"
    )

    assert culture_id == 'pseudo_uniformity'
    assert params == {}
    assert num_voters == 1
    assert num_candidates == 3
    assert len(matrix) == 1
    assert np.allclose(matrix[0], np.array([0.1, 0.2, 0.7]))


def test_import_approval_election_and_check_pseudo(mocker):
    app = """# FILE NAME: example.app
# TITLE: Example
# DATA TYPE: app
# NUMBER ALTERNATIVES: 3
# NUMBER VOTERS: 1
# NUMBER UNIQUE ORDERS: 1
# CULTURE ID: culture_approval
# PARAMS:
1:{1,2}
"""
    mocked_open = mocker.mock_open(read_data=app)
    mocker.patch("builtins.open", mocked_open)

    votes, num_voters, num_candidates, params, culture_id, num_options, quantities, distinct_votes = import_approval_election(
        experiment_id="exp", election_id="example"
    )

    assert num_voters == 1
    assert num_candidates == 3
    assert culture_id == 'culture_approval'
    assert num_options == 1
    assert quantities == [1]
    # votes is a list of sets
    assert isinstance(votes[0], set)
    assert set(votes[0]) == {1, 2}

    # Now test check_if_pseudo for a pseudo culture
    soc_pseudo = """# FILE NAME: example.soc
# TITLE: Example
# DATA TYPE: soc
# NUMBER ALTERNATIVES: 3
# NUMBER VOTERS: 1
# NUMBER UNIQUE ORDERS: 1
# CULTURE ID: pseudo_identity
# PARAMS:
"""
    mocked_open2 = mocker.mock_open(read_data=soc_pseudo)
    mocker.patch("builtins.open", mocked_open2)

    assert check_if_pseudo("exp", "example") is True

    # and for a non-pseudo culture
    soc_non = soc_pseudo.replace('pseudo_identity', 'regular')
    mocked_open3 = mocker.mock_open(read_data=soc_non)
    mocker.patch("builtins.open", mocked_open3)

    assert check_if_pseudo("exp", "example") is False

