import builtins
import sys
import types

import numpy as np
import pytest

import mapof.elections as mapof
from mapof.elections.distances import main_ordinal_distances as mod


def make_election(votes):
    election = mapof.generate_ordinal_election_from_votes(votes)
    election.votes = np.array(votes)
    election.compute_potes()
    return election


@pytest.fixture
def reference_elections():
    election_a = make_election([
        [0, 1, 2],
        [1, 2, 0],
        [2, 0, 1],
    ])
    election_b = make_election([
        [1, 0, 2],
        [2, 1, 0],
        [0, 2, 1],
    ])
    return election_a, election_b


@pytest.fixture
def differing_candidate_elections():
    smaller = make_election([
        [0, 1],
        [1, 0],
    ])
    larger = make_election([
        [0, 1, 2],
        [1, 2, 0],
        [2, 0, 1],
    ])
    equal_a = make_election([
        [0, 1, 2],
        [2, 0, 1],
    ])
    equal_b = make_election([
        [1, 2, 0],
        [2, 0, 1],
    ])
    return smaller, larger, equal_a, equal_b


def test_positionwise_and_pos_swap_distances_cover_cost_tables(reference_elections, monkeypatch):
    election_a, election_b = reference_elections

    def l1_distance(vec_a, vec_b):
        return float(np.sum(np.abs(np.array(vec_a) - np.array(vec_b))))

    positionwise_value, voter_matching = mod.positionwise_distance(
        election_a, election_b, l1_distance
    )
    assert isinstance(positionwise_value, float)
    assert len(voter_matching) == election_a.num_candidates

    monkeypatch.setattr(mod, "swap_distance", lambda va, vb, matching=None: 0)

    pos_swap_value, pos_swap_matching = mod.pos_swap_distance(
        election_a, election_b, l1_distance
    )
    assert isinstance(pos_swap_value, (int, np.integer, float, np.floating))
    assert len(pos_swap_matching) == election_a.num_voters


def test_agg_voterlikeness_and_bordawise_distances(reference_elections):
    election_a, election_b = reference_elections

    def agg_inner(vec_a, vec_b, width):
        assert width == len(vec_a) == len(vec_b)
        diff = float(np.sum(np.abs(vec_a - vec_b)))
        return diff, list(range(width))

    agg_value, agg_mapping = mod.agg_voterlikeness_distance(election_a, election_b, agg_inner)
    assert isinstance(agg_value, float)
    assert agg_mapping == list(range(election_a.num_voters))

    def borda_inner(vec_a, vec_b):
        return float(np.sum(np.abs(vec_a - vec_b)))

    borda_value, borda_mapping = mod.bordawise_distance(election_a, election_b, borda_inner)
    assert isinstance(borda_value, float)
    assert borda_mapping is None


def test_pairwise_and_voterlikeness_distance_use_solver(reference_elections, monkeypatch):
    election_a, election_b = reference_elections
    calls = []

    def fake_solver(matrix1, matrix2, length, inner_distance):
        calls.append((np.array(matrix1).shape, np.array(matrix2).shape, length))
        return float(length + len(calls))

    monkeypatch.setattr(mod, "solve_matching_matrices", fake_solver)

    pairwise_value, pairwise_mapping = mod.pairwise_distance(
        election_a, election_b, lambda x, y: np.linalg.norm(np.array(x) - np.array(y), ord=1)
    )
    assert pairwise_mapping is None
    assert pairwise_value == float(election_a.num_candidates + 1)

    voter_value, voter_mapping = mod.voterlikeness_distance(
        election_a, election_b, lambda x, y: np.linalg.norm(np.array(x) - np.array(y), ord=1)
    )
    assert voter_mapping is None
    assert voter_value == float(election_a.num_voters + 2)

    assert calls == [
        ((election_a.num_candidates, election_a.num_candidates),
         (election_b.num_candidates, election_b.num_candidates),
         election_a.num_candidates),
        ((election_a.num_voters, election_a.num_voters),
         (election_b.num_voters, election_b.num_voters),
         election_a.num_voters),
    ]


def test_swap_distance_bruteforce_and_truncated(reference_elections):
    election_a, election_b = reference_elections

    swap_value, swap_mapping = mod.swap_distance_bf(election_a, election_b)
    assert isinstance(swap_value, (int, np.integer, float, np.floating))
    assert float(swap_value).is_integer()
    assert swap_mapping is None

    truncated_value, truncated_mapping = mod.truncated_swap_distance(election_a, election_b)
    assert isinstance(truncated_value, (int, np.integer, float, np.floating))
    assert float(truncated_value).is_integer()
    assert truncated_mapping is None


def test_swap_distance_fallback_uses_bruteforce(reference_elections, monkeypatch):
    election_a, election_b = reference_elections
    monkeypatch.setattr(mod.utils, "is_module_loaded", lambda name: False)

    bf_value, _ = mod.swap_distance_bf(election_a, election_b)
    fallback_value, fallback_mapping = mod.swap_distance(election_a, election_b)
    assert fallback_mapping is None
    assert fallback_value == bf_value


def test_swap_distance_cppd_branches(differing_candidate_elections, monkeypatch):
    smaller, larger, equal_a, equal_b = differing_candidate_elections

    class DummyCppd:
        def __init__(self):
            self.calls = []

        def tswapd(self, votes_a, votes_b):
            self.calls.append(("tswapd", len(votes_a[0]), len(votes_b[0])))
            return 100 + len(votes_a[0]) + len(votes_b[0])

        def swapd(self, votes_a, votes_b):
            self.calls.append(("swapd", len(votes_a[0]), len(votes_b[0])))
            return 200 + len(votes_a[0]) + len(votes_b[0])

        def speard(self, votes_a, votes_b):
            self.calls.append(("speard", len(votes_a[0]), len(votes_b[0])))
            return 300

    dummy_cppd = DummyCppd()
    monkeypatch.setattr(mod, "cppd", dummy_cppd, raising=False)
    monkeypatch.setattr(mod.utils, "is_module_loaded", lambda name: True)

    val_less, _ = mod.swap_distance(smaller, larger)
    val_greater, _ = mod.swap_distance(larger, smaller)
    val_equal, _ = mod.swap_distance(equal_a, equal_b)

    assert val_less == 100 + smaller.num_candidates + larger.num_candidates
    assert val_greater == 100 + smaller.num_candidates + larger.num_candidates
    assert val_equal == 200 + equal_a.num_candidates + equal_b.num_candidates
    assert dummy_cppd.calls[:3] == [
        ("tswapd", smaller.num_candidates, larger.num_candidates),
        ("tswapd", smaller.num_candidates, larger.num_candidates),
        ("swapd", equal_a.num_candidates, equal_b.num_candidates),
    ]


def test_spearman_distance_fallback_and_cppd(reference_elections, monkeypatch):
    election_a, election_b = reference_elections

    def fake_spearman_solver(votes_a, votes_b, params):
        assert params["voters"] == election_a.num_voters
        assert params["candidates"] == election_a.num_candidates
        return 7.8

    monkeypatch.setattr(mod.ilp_iso, "solve_ilp_spearman_distance", fake_spearman_solver)
    monkeypatch.setattr(mod.utils, "is_module_loaded", lambda name: False)

    fallback_value, fallback_mapping = mod.spearman_distance(election_a, election_b)
    assert fallback_mapping is None
    assert fallback_value == 8

    class DummyCppd:
        def __init__(self):
            self.calls = 0

        def speard(self, votes_a, votes_b):
            self.calls += 1
            return 11

    cpp_stub = DummyCppd()
    monkeypatch.setattr(mod, "cppd", cpp_stub, raising=False)
    monkeypatch.setattr(mod.utils, "is_module_loaded", lambda name: True)

    cpp_value, cpp_mapping = mod.spearman_distance(election_a, election_b)
    assert cpp_mapping is None
    assert cpp_value == 11
    assert cpp_stub.calls == 1


def test_spearman_distance_fastmap_import_error(reference_elections, monkeypatch):
    election_a, election_b = reference_elections
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "fastmap":
            raise ImportError("fastmap missing")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(ImportError):
        mod.spearman_distance_fastmap(election_a, election_b)


def test_spearman_distance_fastmap_success(reference_elections, monkeypatch):
    election_a, election_b = reference_elections
    dummy_module = types.SimpleNamespace(spearman=lambda U, V, method: 13)
    monkeypatch.setitem(sys.modules, "fastmap", dummy_module)

    fastmap_value, fastmap_mapping = mod.spearman_distance_fastmap(
        election_a, election_b, method="bb"
    )
    assert fastmap_mapping is None
    assert fastmap_value == 13


def test_discrete_and_blank_distances(reference_elections, monkeypatch):
    election_a, election_b = reference_elections
    monkeypatch.setattr(mod, "maximum_common_voter_subelection", lambda a, b: 2)

    discrete_value, discrete_mapping = mod.discrete_distance(election_a, election_b)
    assert discrete_mapping is None
    assert discrete_value == election_a.num_voters - 2

    blank_value, blank_mapping = mod.blank_distance(election_a, election_b)
    assert blank_mapping is None
    assert blank_value == 1
