import types

import pytest

from mapof.elections.distances import ilp_other as mod


class FakeVar:
    def __init__(self, name, value=0):
        self.name = name
        self.X = value

    def __add__(self, other):
        if isinstance(other, FakeVar):
            return self.X + other.X
        return self.X + other

    def __radd__(self, other):
        return other + self.X

    def __mul__(self, other):
        if isinstance(other, FakeVar):
            return self.X * other.X
        return self.X * other

    __rmul__ = __mul__

    def __sub__(self, other):
        if isinstance(other, FakeVar):
            return self.X - other.X
        return self.X - other

    def __rsub__(self, other):
        if isinstance(other, FakeVar):
            return other.X - self.X
        return other - self.X


class FakeModel:
    def __init__(self, status, obj_val=0.0, attr_values=None, var_values=None):
        self.status = status
        self.objVal = obj_val
        self.attr_values = attr_values or {}
        self.attr_calls = {}
        self.var_values = var_values or {}
        self.vars = {}
        self.constraints = []
        self.writes = []
        self.parameters = []
        self.objective = None
        self.ModelSense = None

    def setParam(self, name, value):
        self.parameters.append((name, value))

    def addVar(self, vtype=None, name=None, obj=None):
        value = self.var_values.get(name, 0)
        var = FakeVar(name, value)
        self.vars[name] = var
        return var

    def setObjective(self, expr, sense):
        self.objective = (expr, sense)

    def addConstr(self, expr, name=None):
        self.constraints.append((expr, name))

    def write(self, filename):
        self.writes.append(filename)

    def optimize(self):
        # Nothing to do; status/objVal predetermined.
        return

    def update(self):
        return

    def getVarByName(self, name):
        return self.vars[name]

    def getAttr(self, attr):
        values = self.attr_values.get(attr, [0.0])
        idx = self.attr_calls.get(attr, 0)
        value = values[idx] if idx < len(values) else values[-1]
        self.attr_calls[attr] = idx + 1
        return value


def install_fake_model(monkeypatch, config):
    created = []

    def factory(name):
        model = FakeModel(**config)
        created.append(model)
        return model

    monkeypatch.setattr(mod, "Model", factory)
    return created


@pytest.fixture
def fake_grb(monkeypatch):
    attr_ns = types.SimpleNamespace(Runtime="Runtime")
    fake = types.SimpleNamespace(
        BINARY="BINARY",
        INTEGER="INTEGER",
        MINIMIZE="MINIMIZE",
        MAXIMIZE="MAXIMIZE",
        OPTIMAL=1,
        Attr=attr_ns,
    )
    monkeypatch.setattr(mod, "GRB", fake)
    return fake


def test_solve_lp_matching_vector_with_lp_reports_objective(fake_grb, monkeypatch, capsys):
    install_fake_model(monkeypatch, {"status": fake_grb.OPTIMAL, "obj_val": 9.5})
    mod.solve_lp_matching_vector_with_lp([[1, 2], [3, 4]], 2)
    captured = capsys.readouterr()
    assert "Objective Value: 9.5" in captured.out


def test_solve_lp_matching_vector_with_lp_handles_infeasible(fake_grb, monkeypatch, capsys):
    install_fake_model(monkeypatch, {"status": -1, "obj_val": 0})
    mod.solve_lp_matching_vector_with_lp([[1, 2], [3, 4]], 2)
    captured = capsys.readouterr()
    assert "No optimal solution found" in captured.out


def test_solve_lp_matching_interval_returns_scaled_value(fake_grb, monkeypatch):
    instances = install_fake_model(monkeypatch, {"status": fake_grb.OPTIMAL, "obj_val": 60.0})
    result = mod.solve_lp_matching_interval([[1, 2, 3], [4, 5, 6]], 2, 3)
    assert result == pytest.approx(60.0 / 6.0)
    assert instances[0].writes == ['interval.lp', 'interval.mps']


def test_solve_lp_matching_interval_handles_no_solution(fake_grb, monkeypatch, capsys):
    install_fake_model(monkeypatch, {"status": 0, "obj_val": 0.0})
    result = mod.solve_lp_matching_interval([[1]], 1, 1)
    captured = capsys.readouterr()
    assert "No optimal solution found" in captured.out
    assert result is None


def test_solve_lp_file_dodgson_score_returns_objective(fake_grb, monkeypatch):
    install_fake_model(monkeypatch, {"status": fake_grb.OPTIMAL, "obj_val": 7.0})
    N = [2]
    D = [0, 1]
    e = [[[0, 0], [1, 1]]]
    value = mod.solve_lp_file_dodgson_score(N=N, e=e, D=D)
    assert value == 7.0


def test_solve_lp_file_dodgson_score_warns_without_solution(fake_grb, monkeypatch, caplog):
    install_fake_model(monkeypatch, {"status": 0, "obj_val": 0.0})
    N = [1]
    D = [0, 1]
    e = [[[0, 0], [0, 0]]]
    with caplog.at_level("WARNING"):
        assert mod.solve_lp_file_dodgson_score(N=N, e=e, D=D) is None
    assert any("No optimal solution found" in record.message for record in caplog.records)


def test_solve_lp_borda_owa_returns_winners(fake_grb, monkeypatch):
    attr_values = {fake_grb.Attr.Runtime: [1.0, 3.25]}
    var_values = {"y_0": 1, "y_1": 1, "y_2": 0}
    install_fake_model(monkeypatch, {
        "status": fake_grb.OPTIMAL,
        "obj_val": 0.0,
        "attr_values": attr_values,
        "var_values": var_values
    })
    election = types.SimpleNamespace(
        num_voters=2,
        num_candidates=3,
        votes=[[0, 1, 2], [2, 1, 0]]
    )
    owa = [3, 1]
    winners, duration = mod.solve_lp_borda_owa(election, committee_size=2, owa=owa)
    assert winners == [0, 1]
    assert duration == pytest.approx(2.25)


def test_solve_lp_borda_owa_handles_failure(fake_grb, monkeypatch, capsys):
    attr_values = {fake_grb.Attr.Runtime: [0.0, 1.5]}
    install_fake_model(monkeypatch, {
        "status": -1,
        "obj_val": 0.0,
        "attr_values": attr_values
    })
    election = types.SimpleNamespace(
        num_voters=1,
        num_candidates=1,
        votes=[[0]]
    )
    owa = [1]
    winners, duration = mod.solve_lp_borda_owa(election, committee_size=1, owa=owa)
    captured = capsys.readouterr()
    assert "Exception raised during solve" in captured.out
    assert winners is None
    assert duration == pytest.approx(1.5)
