import logging
import os
import csv
import ast
from tqdm import tqdm

try:
    from abcvoting.preferences import Profile
    from abcvoting import abcrules
except ImportError:
    logging.warning("ABC Voting library not found. Some features may not work.")
    Profile = None
    abcrules = None


def export_committees_to_file(experiment_id, rule_name, all_winning_committees):
    path = os.path.join(os.getcwd(), "experiments", experiment_id, 'features',
                        f'{rule_name}.csv')
    with open(path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(["election_id", "committee"])
        for election_id in all_winning_committees:
            writer.writerow([election_id, all_winning_committees[election_id]])


def import_committees_from_file(experiment_id, rule_name):
    all_winning_committees = {}
    path = os.path.join(os.getcwd(), "experiments", experiment_id, 'features',
                        f'{rule_name}.csv')
    with open(path, 'r', newline='') as csv_file:
        header = [h.strip() for h in csv_file.readline().split(';')]
        reader = csv.DictReader(csv_file, fieldnames=header, delimiter=';')
        for row in reader:
            try:
                winning_committees = ast.literal_eval(row['committee'])
            except:
                winning_committees = [set(row['committee'][2:-2].split(', '))]
            if len(winning_committees) == 0:
                winning_committees = [set()]
            all_winning_committees[row['election_id']] = winning_committees
    return all_winning_committees


def compute_abcvoting_rule_for_single_election(
        election=None,
        rule_name=None,
        committee_size=1,
        resolute=False
):
    profile = Profile(election.num_candidates)
    profile.add_voters(election.votes)

    try:
        winning_committees = abcrules.compute(rule_name, profile, committee_size,
                                              algorithm="gurobi", resolute=resolute)
    except Exception:
        try:
            winning_committees = abcrules.compute(rule_name, profile, committee_size,
                                                  resolute=resolute)
        except:
            winning_committees = {}

    clean_winning_committees = []
    for committee in winning_committees:
        clean_winning_committees.append(set(committee))

    election.winning_committee[rule_name] = clean_winning_committees[0]

    return clean_winning_committees


def compute_abcvoting_rule(experiment=None, rule_name=None, committee_size=1, resolute=False):
    all_winning_committees = {}
    for election in tqdm(experiment.instances.values()):
        clean_winning_committees = compute_abcvoting_rule_for_single_election(
            election=election,
            rule_name=rule_name,
            committee_size=committee_size,
            resolute=resolute
        )

        all_winning_committees[election.election_id] = clean_winning_committees

    if experiment.is_exported:
        export_committees_to_file(experiment.experiment_id, rule_name, all_winning_committees)

