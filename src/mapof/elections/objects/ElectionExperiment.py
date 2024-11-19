import ast
import csv
import logging
import os
import time
import warnings
from abc import ABCMeta, abstractmethod

import mapof.core.persistence.experiment_exports as exports
import mapof.core.printing as pr
from mapof.core.features.register import (
    registered_experiment_features,
    features_embedding_related
)
from mapof.core.objects.Experiment import Experiment
from mapof.core.utils import get_instance_id
from tqdm import tqdm

import mapof.elections.other.approval_rules as rules
from mapof.elections.cultures.register import (
    registered_ordinal_election_cultures,
    registered_pseudo_ordinal_cultures
)
from mapof.elections.distances import get_distance
from mapof.elections.features.register import (
    features_with_params,
    features_rule_related
)
from mapof.elections.objects.ApprovalElection import ApprovalElection
from mapof.elections.objects.ElectionFamily import ElectionFamily
from mapof.elections.objects.ElectionFeatures import (
    ST_KEY,
    AN_KEY,
    ID_KEY,
    UN_KEY
)
from mapof.elections.objects.OrdinalElection import OrdinalElection

try:
    from sklearn.manifold import MDS
    from sklearn.manifold import TSNE
    from sklearn.manifold import SpectralEmbedding
    from sklearn.manifold import LocallyLinearEmbedding
    from sklearn.manifold import Isomap
except ImportError as error:
    MDS = None
    TSNE = None
    SpectralEmbedding = None
    LocallyLinearEmbedding = None
    Isomap = None
    print(error)


class ElectionExperiment(Experiment):
    __metaclass__ = ABCMeta
    """Abstract set of instances."""

    @abstractmethod
    def add_folders_to_experiment(self):
        pass

    @abstractmethod
    def add_feature(self, name, function):
        pass

    @abstractmethod
    def add_culture(self, name, function):
        pass

    def __init__(self, is_shifted=False, **kwargs):
        self.is_shifted = is_shifted
        self.default_num_candidates = 10
        self.default_num_voters = 100
        self.default_committee_size = 1
        self.all_winning_committees = {}
        super().__init__(**kwargs)

    def __getattr__(self, attr):
        if attr == 'elections':
            return self.instances
        elif attr == 'num_elections':
            return self.num_instances
        else:
            return self.__dict__[attr]

    def __setattr__(self, name, value):
        if name == "elections":
            self.instances = value
        elif name == "num_elections":
            self.num_instances = value
        else:
            self.__dict__[name] = value

    def add_instances_to_experiment(self) -> None:
        """
        Add instances to the experiment.

        Returns:
            None
        """
        instances = {}

        for family_id in self.families:
            single = self.families[family_id].single
            ids = []
            for j in range(self.families[family_id].size):
                instance_id = get_instance_id(single, family_id, j)
                if self.instance_type == 'ordinal':
                    instance = OrdinalElection(self.experiment_id, instance_id,
                                               is_imported=True,
                                               fast_import=self.fast_import,
                                               with_matrix=self.with_matrix,
                                               label=self.families[family_id].label)
                elif self.instance_type == 'approval':
                    instance = ApprovalElection(self.experiment_id, instance_id,
                                                is_imported=True,
                                                fast_import=self.fast_import,
                                                label=self.families[family_id].label)
                else:
                    instance = None

                instances[instance_id] = instance
                ids.append(str(instance_id))

            self.families[family_id].election_ids = ids

        return instances

    def set_default_num_candidates(self, num_candidates: int) -> None:
        """
        Sets default number of candidates

        Parameters
        ----------
            num_candidates : int
                Number of candidates.

        Returns
        -------
            None
        """
        self.default_num_candidates = num_candidates

    def set_default_num_voters(self, num_voters: int) -> None:
        """
        Sets default number of voters

        Parameters
        ----------
            num_voters : int
                Number of voters.

        Returns
        -------
            None
        """
        self.default_num_voters = num_voters

    def set_default_committee_size(self, committee_size: int) -> None:
        """
        Sets default size of the committee

        Parameters
        ----------
            committee_size : int
                Committee size.

        Returns
        -------
            None
        """
        self.default_committee_size = committee_size

    def add_election_from_matrix(self,
                                 frequency_matrix,
                                 **kwargs):

        if len(frequency_matrix) != len(frequency_matrix[0]):
            raise ValueError("Matrix is not square")

        self.add_election(
            num_candidates=len(frequency_matrix),
            frequency_matrix=frequency_matrix,
            culture_id='frequency_matrix',
            **kwargs
        )

    def add_election(self,
                     culture_id="none",
                     label=None,
                     color="black",
                     alpha: float = 1.,
                     show: bool = True,
                     marker='x',
                     ms=20,
                     starting_from: int = 0,
                     size: int = 1,
                     num_candidates: int = None,
                     num_voters: int = None,
                     election_id: str = None,  # deprecated
                     instance_id: str = None,
                     frequency_matrix=None,
                     is_temporary: bool = False,
                     params: dict = None,
        ):
        """
        Adds election to the experiment.

        Parameters
        ----------
            culture_id : str
                Culture id.
            label : str
                Label.
            color
                Color.
            alpha : float
                Alpha.
            show : bool
                If true the election is shown.
            marker : str
                Marker.
            ms : int
                Marker size.
            starting_from : int
                Starting index.
            size : int
                Size.
            num_candidates : int
                Number of candidates.
            num_voters : int
                Number of voters.
            election_id : str
                Election id.
            instance_id : str
                Instance id.
            frequency_matrix : list
                Frequency matrix.
            is_temporary : bool
                If true the election is temporary.
            params : dict
                Model parameters.

        Returns
        -------
            list
                List of IDs of added instances.
        """

        if instance_id is None:
            instance_id = election_id

        if num_candidates is None:
            num_candidates = self.default_num_candidates

        if num_voters is None:
            num_voters = self.default_num_voters

        return self.add_family(culture_id=culture_id,
                               size=size,
                               label=label,
                               color=color,
                               alpha=alpha,
                               show=show,
                               marker=marker,
                               ms=ms,
                               starting_from=starting_from,
                               family_id=instance_id,
                               num_candidates=num_candidates,
                               num_voters=num_voters,
                               frequency_matrix=frequency_matrix,
                               is_temporary=is_temporary,
                               single=True,
                               params=params)

    def add_family(self,
                   culture_id: str = "none",
                   size: int = 1,
                   label: str = None,
                   color: str = "black",
                   alpha: float = 1.,
                   show: bool = True,
                   marker: str = 'o',
                   ms: int = 20,
                   starting_from: int = 0,
                   num_candidates: int = None,
                   num_voters: int = None,
                   frequency_matrix=None,
                   is_temporary: bool = False,
                   family_id: str = None,
                   single: bool = False,
                   path: dict = None,
                   params: dict = None,
        ) -> list:
        """
        Adds family of elections to the experiment.

        Parameters
        ----------
            culture_id : str
                Culture id.
            label : str
                Label.
            color
                Color.
            alpha : float
                Alpha (i.e., transparency).
            show : bool
                If true the family is shown.
            marker : str
                Marker.
            ms : int
                Marker size.
            starting_from : int
                Starting index.
            size : int
                Size.
            num_candidates : int
                Number of candidates.
            num_voters : int
                Number of voters.
            frequency_matrix : list
                Frequency matrix.
            is_temporary : bool
                If true the election is temporary.
            family_id : str
                Family id.
            single : bool
                If true only one election is added.
            path : dict
                Path.
            params : dict
                Model parameters.

        Returns
        -------
            list
                List of IDs of added instances.

        """

        if num_candidates is None:
            num_candidates = self.default_num_candidates

        if num_voters is None:
            num_voters = self.default_num_voters

        if self.families is None:
            self.families = {}

        if params is None:
            params = {}

        if family_id is None:
            family_id = culture_id + '_' + str(num_candidates) + '_' + str(num_voters)
            if culture_id in {'urn'} and params.get('alpha') is not None:
                family_id += '_' + str(float(params['alpha']))
            elif culture_id in {'mallows'} and params.get('phi') is not None:
                family_id += '_' + str(float(params['phi']))
            elif culture_id in {'norm-mallows', 'norm-mallows_matrix'} \
                    and params.get('normphi') is not None:
                family_id += '_' + str(float(params['normphi']))
            elif culture_id in {'euclidean'} and params.get('dim') is not None \
                    and params.get('space') is not None:
                family_id += '_' + str(int(params['dim'])) + '_' + str(params['space'])

        elif label is None:
            label = family_id

        self.families[family_id] = ElectionFamily(culture_id=culture_id,
                                                  family_id=family_id,
                                                  params=params,
                                                  label=label,
                                                  color=color,
                                                  alpha=alpha,
                                                  show=show,
                                                  size=size,
                                                  marker=marker,
                                                  ms=ms,
                                                  starting_from=starting_from,
                                                  num_candidates=num_candidates,
                                                  num_voters=num_voters,
                                                  path=path,
                                                  single=single,
                                                  instance_type=self.instance_type,
                                                  frequency_matrix=frequency_matrix,
                                                  is_temporary=is_temporary,
                                                )

        self.num_families = len(self.families)
        self.num_elections = sum([self.families[family_id].size for family_id in self.families])
        self.main_order = [i for i in range(self.num_elections)]

        new_instances = self.families[family_id].prepare_family(
            is_exported=self.is_exported,
            experiment_id=self.experiment_id,
            instance_type=self.instance_type)

        for instance_id in new_instances:
            self.instances[instance_id] = new_instances[instance_id]

        self.families[family_id].instance_ids = list(new_instances.keys())

        if self.is_exported and not is_temporary:
            self._update_map_csv()

        return list(new_instances.keys())

    def add_existing_family_from_dir(
            self,
            dir: str = None,
            culture_id: str = None,
            **kwargs
    ) -> list:
        """
        Adds family of elections to the experiment from the given directory.

        Parameters
        ----------
            dir : str
                Directory.
            culture_id : str
                Culture id.
            **kwargs : dict
                Additional parameters.

        Returns
        -------
            list
                List of the families.

        """
        if dir is None:
            logging.warning('dir not specified')
        if culture_id is None:
            logging.warning('pseudo_culture_id not specified')

        # Copy instances from dir to /elections

        directory_in = dir
        directory_out = os.path.join(os.getcwd(),
                                     "experiments",
                                     self.experiment_id,
                                     'elections')

        # List all files in the given directory
        files = [f for f in os.listdir(directory_in) if
                 os.path.isfile(os.path.join(directory_in, f))]

        # Sort the files for consistency
        files.sort()

        # Rename each file
        for idx, file_name in enumerate(files):
            # Create the new file name
            # new_file_name = f"{pseudo_culture_id}_{idx}{os.path.splitext(file_name)[1]}"
            new_file_name = f"{culture_id}_{idx}.soc"

            # Form the full old and new paths
            old_path = os.path.join(directory_in, file_name)
            new_path = os.path.join(directory_out, new_file_name)

            # Rename the file
            os.rename(old_path, new_path)
            print(f"Renaming: {file_name} -> {new_file_name}")

        return self.add_family(culture_id=culture_id, **kwargs)

    def _update_map_csv(self):
        families = {}
        path_to_file = os.path.join(os.getcwd(), 'experiments', self.experiment_id, 'map.csv')
        with open(path_to_file, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')

            all_fields = ['size',
                          'num_candidates',
                          'num_voters',
                          'culture_id',
                          'params',
                          'family_id',
                          'label',
                          'color',
                          'alpha',
                          'marker',
                          'ms',
                          'path'
                          ]

            writer.writerow(all_fields)

            for family in self.families.values():
                if not family.is_temporary:
                    all_values = [family.size,
                                  family.num_candidates,
                                  family.num_voters,
                                  family.culture_id,
                                  family.params,
                                  family.family_id,
                                  family.label,
                                  family.color,
                                  family.alpha,
                                  family.marker,
                                  family.ms,
                                  family.path]

                    writer.writerow(all_values)

        return families

    def add_empty_family(
            self,
            culture_id: str = "none",
            label: str = None,
            color: str = "black",
            alpha: float = 1.,
            show: bool = True,
            marker: str = 'o',
            num_candidates: int = None,
            num_voters: int = None,
            family_id: str = None
    ):
        """
        Adds an empty family of elections to the experiment.

        Parameters
        ----------
            culture_id : str
                Culture id.
            label : str
                Label.
            color : str
                Color.
            alpha : float
                Alpha.
            show : bool
                If true the family is shown.
            marker : str
                Marker.
            num_candidates : int
                Number of candidates.
            num_voters : int
                Number of voters.
            family_id : str
                Family id.
        """

        if label is None:
            label = family_id
        self.families[family_id] = ElectionFamily(culture_id=culture_id,
                                                  family_id=family_id,
                                                  label=label,
                                                  color=color,
                                                  alpha=alpha,
                                                  show=show,
                                                  size=0,
                                                  marker=marker,
                                                  num_candidates=num_candidates,
                                                  num_voters=num_voters,
                                                  instance_type=self.instance_type)

        self.families[family_id].prepare_family(
            is_exported=self.is_exported,
            experiment_id=self.experiment_id)

        return self.families[family_id]

    def prepare_elections(self, export_points=False, is_aggregated=True) -> None:
        """
        Prepares elections for a given experiment.

        Parameters
        ----------
        export_points : bool
            Whether to store points in the instance.
        is_aggregated : bool
            Whether to aggregate the instances.

        Returns
        -------
            None
        """
        self.export_points = export_points
        self.is_aggregated = is_aggregated

        if self.instances is None:
            self.instances = {}

        for family_id in tqdm(self.families, desc="Preparing instances"):

            if self.instance_type == 'ordinal' and \
                    self.families[family_id].culture_id not in registered_pseudo_ordinal_cultures and \
                    self.families[family_id].culture_id not in registered_ordinal_election_cultures:
                continue

            new_instances = self.families[family_id].prepare_family(
                is_exported=self.is_exported,
                experiment_id=self.experiment_id,
                export_points=export_points,
                is_aggregated=is_aggregated,
                instance_type=self.instance_type,
            )

            for instance_id in new_instances:
                self.instances[instance_id] = new_instances[instance_id]

    def compute_voting_rule(self, method=None, committee_size=1) -> None:
        """
        Computes voting rule for all elections in the experiment.

        Parameters
        ----------
            method : str
                Name of the boting rule to be computed.
            committee_size : int
                Size of the committee.

        Returns
        -------
            None
        """
        for election_id in self.elections:
            self.elections[election_id].compute_voting_rule(
                method=method, committee_size=committee_size)

    def compute_alternative_winners(self, method=None, committee_size=None, num_parties=None):
        for election_id in self.elections:
            for party_id in range(num_parties):
                self.elections[election_id].compute_alternative_winners(
                    method=method, party_id=party_id, committee_size=committee_size)

    def get_distance(
            self,
            election_1,
            election_2,
            distance_id: str = None,
            **kwargs
    ) -> float or (float, list):
        return get_distance(election_1, election_2, distance_id)

    def print_matrix(self, **kwargs):
        pr.print_matrix(experiment=self, **kwargs)

    def import_controllers(self) -> list:
        """
        Import controllers from a file

        Returns
        -------
            list
                List of families.
        """

        families = {}

        path = os.path.join(os.getcwd(), 'experiments', self.experiment_id, 'map.csv')
        with open(path, 'r') as file_:

            header = [h.strip() for h in file_.readline().split(';')]
            reader = csv.DictReader(file_, fieldnames=header, delimiter=';')

            all_num_candidates = []
            all_num_voters = []

            starting_from = 0
            for row in reader:

                culture_id = None
                params = None
                size = None
                num_candidates = None
                num_voters = None
                family_id = None

                print_params = {}

                if 'culture_id' in row.keys():
                    culture_id = str(row['culture_id']).strip()

                if 'family_id' in row.keys():
                    family_id = str(row['family_id'])

                if 'params' in row.keys():
                    params = ast.literal_eval(str(row['params']))

                if 'size' in row.keys():
                    size = int(row['size'])

                if 'num_candidates' in row.keys():
                    num_candidates = int(row['num_candidates'])

                if 'num_voters' in row.keys():
                    num_voters = int(row['num_voters'])

                if 'path' in row.keys():
                    path = ast.literal_eval(str(row['path']))

                if 'label' in row.keys():
                    print_params['label'] = str(row['label'])
                if 'alpha' in row.keys():
                    print_params['alpha'] = float(row['alpha'])
                if 'marker' in row.keys():
                    print_params['marker'] = str(row['marker']).strip()
                if 'ms' in row.keys():
                    print_params['ms'] = int(row['ms'])
                if 'color' in row.keys():
                    print_params['color'] = str(row['color']).strip()

                single = size == 1

                families[family_id] = ElectionFamily(culture_id=culture_id,
                                                     family_id=family_id,
                                                     params=params,
                                                     size=size,
                                                     starting_from=starting_from,
                                                     num_candidates=num_candidates,
                                                     num_voters=num_voters,
                                                     path=path,
                                                     single=single,
                                                     **print_params
                                                     )
                starting_from += size

                all_num_candidates.append(num_candidates)
                all_num_voters.append(num_voters)

            _check_if_all_equal(all_num_candidates, 'num_candidates')
            _check_if_all_equal(all_num_voters, 'num_voters')

            self.num_families = len(families)
            self.num_elections = sum([families[family_id].size for family_id in families])
            self.main_order = [i for i in range(self.num_elections)]

        return families

    def compute_feature(
            self,
            feature_id: str = None,
            feature_params: dict = None,
            overwrite: bool = False,
            saveas: str = None,
            **kwargs
    ) -> dict:
        """
        Computes a feature for each in instances in the experiment.

        Parameters
        ----------
            feature_id : str
                The id of the feature to compute.
            feature_params : dict
                The parameters of the feature to compute.
            overwrite : bool
                Whether to overwrite the feature if it already exists.
            saveas : str

        Returns
        -------
            dict
                A dictionary with the computed feature for each instance.
        """

        if feature_params is None:
            feature_params = {}

        if feature_id in features_rule_related:
            feature_long_id = f'{feature_id}_{feature_params["rule"]}'
        elif feature_id in features_embedding_related:
            feature_long_id = f'{feature_id}_{self.embedding_id}'
        else:
            feature_long_id = feature_id

        num_iterations = feature_params.get('num_iterations', 1)

        feature_dict = {'value': {}, 'time': {}}

        if feature_id in registered_experiment_features:

            feature = registered_experiment_features[feature_id]

            solution_dict = feature(self, election_ids=list(self.instances), **kwargs)

            for instance_id in tqdm(self.instances, desc='Computing experiment feature'):

                for key in solution_dict[instance_id]:
                    if key not in feature_dict:
                        feature_dict[key] = {}

                feature_dict['value'][instance_id] = solution_dict[instance_id]
                if solution_dict[instance_id] is None:
                    feature_dict['time'][instance_id] = None
                else:
                    feature_dict['time'][instance_id] = 0

        else:

            for instance_id in tqdm(self.instances, desc=f"{feature_long_id}"):
                instance = self.elections[instance_id]

                start = time.time()
                solution = None
                for _ in range(num_iterations):

                    if feature_id in features_with_params:
                        solution = instance.get_feature(feature_id, feature_long_id,
                                                        feature_params=feature_params)

                    else:
                        solution = instance.get_feature(feature_id, feature_long_id,
                                                        overwrite=overwrite, **kwargs)
                        value = None

                total_time = time.time() - start
                total_time /= num_iterations

                if solution is not None:
                    if type(solution) is dict:
                        if 'value' not in solution:
                            solution['value'] = None
                        for key in solution:
                            if key not in feature_dict:
                                feature_dict[key] = {}
                            feature_dict[key][instance_id] = solution[key]
                    else:
                        feature_dict['value'][instance_id] = solution
                    feature_dict['time'][instance_id] = total_time
                else:
                    feature_dict['value'][instance_id] = value
                    feature_dict['time'][instance_id] = total_time

        if saveas is None:
            saveas = feature_long_id

        if self.is_exported:
            exports.export_feature_to_file(self,
                                           feature_id=feature_id,
                                           feature_dict=feature_dict,
                                           saveas=saveas)

        self.features[saveas] = feature_dict
        return feature_dict

    def compute_rules(
            self,
            list_of_rules: list,
            committee_size: int = 10,
            resolute: bool = False
    ) -> None:
        """
        Computes the winning committees for a list of rules.

        Parameters
        ----------
            list_of_rules : list
                A list of rules to compute the winning committees for.
            committee_size : int
                The size of the winning committees.
            resolute : bool
                Whether to compute the resolute committees.

        Returns
        -------
            None
        """

        for rule_name in list_of_rules:
            print('Computing', rule_name)
            rules.compute_abcvoting_rule(
                experiment=self,
                rule_name=rule_name,
                committee_size=committee_size,
                resolute=resolute)

    def import_committees(self, list_of_rules) -> None:
        """
        Imports the winning committees for a list of rules.

        Parameters
        ----------
            list_of_rules : list
                A list of rules to import the winning committees for.

        Returns
        -------
            None
        """
        for rule_name in list_of_rules:
            self.all_winning_committees[rule_name] = rules.import_committees_from_file(
                experiment_id=self.experiment_id, rule_name=rule_name)

    def add_election_to_family(self, election=None, family_id=None) -> None:
        """
        Adds an election to a family.

        Parameters
        ----------
            election : Election
                The election to add to the family.
            family_id : str
                The id of the family to add the election to.

        Returns
        -------
            None
        """
        election.instance_id = f'{self.families[family_id]}_{self.families[family_id].size}'
        self.instances[election.instance_id] = election
        self.families[family_id].add_election(election)

    def prepare_election_features(self):
        for election in self.instances.items():
            election[1].election_features.votes = election[1].votes
            election[1].election_features.num_candidates = election[1].num_candidates
            election[1].election_features.num_voters = election[1].num_voters
            election[1].election_features.calculate_all()

    def prepare_compass_dictionary(self):
        for election in self.instances.items():
            election[1].election_features.votes = election[1].votes
            election[1].election_features.num_candidates = election[1].num_candidates
            election[1].election_features.num_voters = election[1].num_voters
            election[1].election_features.compass_points['ST'] = self.instances[
                ST_KEY + str(election[1].num_candidates)]
            election[1].election_features.compass_points['AN'] = self.instances[
                AN_KEY + str(election[1].num_candidates)]
            election[1].election_features.compass_points['ID'] = self.instances[
                ID_KEY + str(election[1].num_candidates)]
            election[1].election_features.compass_points['UN'] = self.instances[
                UN_KEY + str(election[1].num_candidates)]

    def calculate_dap(self, id):
        dap = list()
        dap.append(self.features['Diversity'][id])
        dap.append(self.features['Agreement'][id])
        dap.append(self.features['Polarization'][id])
        return dap

    def calculate_features_vector(self, id, features_list: list):
        vector = list()
        if 'd' in features_list:
            vector.append(self.features['Diversity'][id])
        if 'a' in features_list:
            vector.append(self.features['Agreement'][id])
        if 'p' in features_list:
            vector.append(self.features['Polarization'][id])
        if 'e' in features_list:
            vector.append(self.features['Entropy'][id])
        if 'e2' in features_list:
            vector.append(self.features['Entropy'][id] * self.features['Entropy'][id])
        if 'cds' in features_list:
            vector.append(self.features['CandidateDistanceStd'][id])
        return vector

    def prepare_election_sizes(self):
        for election in self.instances.items():
            self.election_sizes.add(election[1].num_candidates)

    def prepare_feature_vectors(self, features: list):
        for election in self.instances.items():
            election[1].election_features.votes = election[1].votes
            election[1].election_features.num_candidates = election[1].num_candidates
            election[1].election_features.num_voters = election[1].num_voters
            election[1].election_features.features_vector = self.calculate_features_vector(
                election[1].election_id,
                features)

    def prepare_instances(self):
        return self.prepare_elections()

    def add_instance(self):
        return self.add_election()

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__.update(state)


def _check_if_all_equal(values, subject):
    if any(x != values[0] for x in values):
        text = f'Not all {subject} values are equal!'
        warnings.warn(text)
