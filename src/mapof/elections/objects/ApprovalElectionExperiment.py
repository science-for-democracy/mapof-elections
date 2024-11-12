import csv
from abc import ABC
from pathlib import Path

import numpy as np
from mapof.core.matchings import solve_matching_vectors
from tqdm import tqdm

import mapof.elections.cultures as cultures
import mapof.elections.distances as distances
import mapof.elections.features as features
from mapof.elections.objects.ElectionExperiment import ElectionExperiment

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


class ApprovalElectionExperiment(ElectionExperiment, ABC):
    """ Abstract set of approval elections."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_culture(self, name, function):
        cultures.add_approval_culture(name, function)

    def add_feature(self, name, function):
        features.add_approval_feature(name, function)

    def add_distance(self, name, function):
        distances.add_approval_distance(name, function)

    def compute_distance_between_rules(
            self,
            list_of_rules=None,
            printing=False,
            distance_id=None,
            committee_size=10
    ):

        self.import_committees(list_of_rules=list_of_rules)

        path = Path.cwd() / "experiments"/ f'{self.experiment_id}' / '..' / \
                            'rules_output' / 'distances' / f'{distance_id}.csv'

        with open(path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(["election_id_1", "election_id_2", "distance", "time"])

            for i, r1 in enumerate(list_of_rules):
                for j, r2 in enumerate(list_of_rules):
                    if i < j:
                        if printing:
                            print(r1, r2)
                        all_distance = []
                        for election_id in self.elections:
                            com1 = self.all_winning_committees[r1][
                                election_id][0]
                            com2 = self.all_winning_committees[r2][
                                election_id][0]

                            if distance_id == 'discrete':
                                distance = len(com1.symmetric_difference(com2))
                            elif distance_id in ['hamming', 'jaccard']:
                                cand_dist = np.zeros([committee_size, committee_size])
                                self.elections[election_id].compute_reverse_approvals()
                                for k1, c1 in enumerate(com1):
                                    for k2, c2 in enumerate(com2):

                                        ac1 = self.elections[election_id].reverse_approvals[c1]
                                        ac2 = self.elections[election_id].reverse_approvals[c2]
                                        if distance_id == 'hamming':
                                            cand_dist[k1][k2] = len(ac1.symmetric_difference(ac2))
                                        elif distance_id == 'jaccard':
                                            if len(ac1.union(ac2)) != 0:
                                                cand_dist[k1][k2] = 1 - len(
                                                    ac1.intersection(ac2)) / len(ac1.union(ac2))
                                distance, _ = solve_matching_vectors(cand_dist)
                                distance /= committee_size
                                if printing:
                                    print(distance)
                            all_distance.append(distance)
                        mean = sum(all_distance) / self.num_elections
                        writer.writerow([r1, r2, mean, 0.])

    def compute_rule_features(self,
                              feature_id=None,
                              list_of_rules=None,
                              feature_params=None,
                              **kwargs):
        if feature_params is None:
            feature_params = {}

        self.import_committees(list_of_rules=list_of_rules)

        for election_id in self.elections:
            self.elections[election_id].winning_committee = {}

        for r in list_of_rules:
            for election_id in self.elections:
                self.elections[election_id].winning_committee[r] = \
                    self.all_winning_committees[r][election_id][0]

        for rule in tqdm(list_of_rules):
            feature_params['rule'] = rule
            self.compute_feature(feature_id=feature_id, feature_params=feature_params, **kwargs)

    def print_latex_table(self,
                          feature_id=None,
                          column_id='value',
                          list_of_rules=None,
                          list_of_models=None):

        features = {}
        for rule in list_of_rules:
            features[rule] = self.import_feature(feature_id, column_id=column_id, rule=rule)

        results = {}
        for model in list_of_models:
            results[model] = {}
            for rule in list_of_rules:
                feature = features[rule]
                total_value = 0
                ctr = 0
                for instance in feature:
                    if model in instance:
                        total_value += feature[instance]
                        ctr += 1
                avg_value = round(total_value / ctr, 2)
                results[model][rule] = avg_value

        print("\\toprule")
        print("rule", end=" ")
        for model in list_of_models:
            print(f'& {model}', end=" ")
        print("\\\\ \\midrule")

        for rule in list_of_rules:
            print(rule, end=" ")
            for model in list_of_models:
                print(f'& {results[model][rule]}', end=" ")
            # print("")
            print("\\\\ \\midrule")

    def print_latex_multitable(self,
                               features_id=None,
                               columns_id=None,
                               list_of_rules=None,
                               list_of_models=None):

        all_results = {}
        for feature_id, column_id in zip(features_id, columns_id):
            features = {}
            for rule in list_of_rules:
                features[rule] = self.import_feature(feature_id, column_id=column_id, rule=rule)

            results = {}
            for model in list_of_models:
                results[model] = {}
                for rule in list_of_rules:
                    feature = features[rule]
                    total_value = 0
                    ctr = 0
                    for instance in feature:
                        if model.lower() in instance.lower():
                            total_value += feature[instance]
                            ctr += 1
                    if ctr == 0:
                        avg_value = -1
                    else:
                        avg_value = round(total_value / ctr, 2)
                    results[model][rule] = avg_value
            all_results[f'{feature_id}_{column_id}'] = results

        for rule in list_of_rules:
            print(rule, end=" ")
            for model in list_of_models:
                print(f'&', end=" ")
                for feature_id, column_id in zip(features_id, columns_id):
                    print(f'{all_results[f"{feature_id}_{column_id}"][model][rule]}', end=" \ ")
            print("\\\\ \\midrule")

    def add_folders_to_experiment(self) -> None:
        """
        Creates the folders within the experiment directory.

        Returns
        -------
            None
        """

        dirs = ["experiments"]
        for ddir in dirs:
            (Path.cwd() / ddir).mkdir(exist_ok=True)

        (Path.cwd() / "experiments" / self.experiment_id).mkdir(exist_ok=True)

        list_of_folders = ['distances',
                           'features',
                           'coordinates',
                           'elections',
                           ]

        for folder_name in list_of_folders:
            to_check = Path.cwd() / "experiments" / self.experiment_id / folder_name
            to_check.mkdir(exist_ok=True)

        path = Path.cwd() / "experiments" / self.experiment_id / "map.csv"
        if not path.exists():
            with open(path, 'w') as file_csv:
                file_csv.write(
                    "size;num_candidates;num_voters;culture_id;params;family_id;"
                    "label;color;alpha;marker;ms;path;show\n"
                )
