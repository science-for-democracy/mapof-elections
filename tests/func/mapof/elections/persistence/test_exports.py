
import os
from mapof.elections.persistence.election_exports import \
    export_distances, \
    export_coordinates


# Mock Election class to simulate the behavior
class MockElection:
    def __init__(self, election_id, experiment_id, distances=None, coordinates=None):
        self.election_id = election_id
        self.experiment_id = experiment_id
        self.distances = distances
        self.coordinates = coordinates


def test_export_distances(mocker):
    # Arrange
    # Mocking an election object with distances
    mock_election = MockElection(
        election_id='election123',
        experiment_id='experiment123',
        distances={
            'vote': [[0.0, 1.0], [1.0, 0.0]]  # Example distance frequency_matrix
        }
    )

    # Mock the 'open' function to avoid file creation
    mocked_open = mocker.patch("builtins.open", mocker.mock_open())

    # Mock csv.writer to capture its output
    mocked_csv_writer = mocker.patch("csv.writer")

    # Act
    export_distances(mock_election, object_type='vote')

    # Assert
    # Check if the file was opened with the correct path and mode
    expected_path = os.path.join(
        os.getcwd(), "experiments", mock_election.experiment_id, "distances",
        f'{mock_election.election_id}_vote.csv'
    )
    mocked_open.assert_called_once_with(expected_path, 'w', newline='')

    # Verify the CSV writer was called with the correct delimiter
    mocked_csv_writer.assert_called_once_with(mocked_open(), delimiter=';')

    # Get the writer instance used for writing rows
    writer_instance = mocked_csv_writer()

    # Check that the correct rows were written
    expected_calls = [
        mocker.call(["v1", "v2", "distance"]),  # Header row
        mocker.call([0, 0, '0.0']),             # First data row
        mocker.call([0, 1, '1.0']),             # Second data row
        mocker.call([1, 0, '1.0']),             # Third data row
        mocker.call([1, 1, '0.0'])              # Fourth data row
    ]

    writer_instance.writerow.assert_has_calls(expected_calls, any_order=False)


def test_export_coordinates(mocker):
    # Arrange
    # Mocking an election object with coordinates
    mock_election = MockElection(
        election_id='election123',
        experiment_id='experiment123',
        coordinates={
            'vote': [[1.0, 2.0], [3.0, 4.0]]  # Example coordinates
        }
    )

    # Mock the 'open' function to avoid file creation
    mocked_open = mocker.patch("builtins.open", mocker.mock_open())

    # Mock csv.writer to capture its output
    mocked_csv_writer = mocker.patch("csv.writer")

    # Act
    export_coordinates(mock_election, object_type='vote')

    # Assert
    # Check if the file was opened with the correct path and mode
    expected_path = os.path.join(
        os.getcwd(), "experiments", mock_election.experiment_id, "coordinates",
        f'{mock_election.election_id}_vote.csv'
    )
    mocked_open.assert_called_once_with(expected_path, 'w', newline='')

    # Verify the CSV writer was called with the correct delimiter
    mocked_csv_writer.assert_called_once_with(mocked_open(), delimiter=';')

    # Get the writer instance used for writing rows
    writer_instance = mocked_csv_writer()

    # Check that the correct rows were written
    expected_calls = [
        mocker.call(["vote_id", "x", "y"]),  # Header row
        mocker.call([0, '1.0', '2.0']),      # First data row
        mocker.call([1, '3.0', '4.0'])       # Second data row
    ]

    writer_instance.writerow.assert_has_calls(expected_calls, any_order=False)
