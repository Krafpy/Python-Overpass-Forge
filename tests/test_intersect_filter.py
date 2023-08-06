from overpass_builder.filters import IntersectsWith
from overpass_builder.statements import Statement
from overpass_builder.variables import VariableManager
import pytest

def test_one_intersections():
    a = Statement()
    vars = VariableManager()
    name_a = vars.add_statement(a)
    assert IntersectsWith(a).compile(vars) == f".{name_a}"

def test_two_intersections():
    a = Statement()
    b = Statement()
    vars = VariableManager()
    name_a = vars.add_statement(a)
    name_b = vars.add_statement(b)
    assert IntersectsWith(a, b).compile(vars) == f".{name_a}.{name_b}"

def test_requires_variable():
    a = Statement()
    b = Statement()
    vars = VariableManager()
    vars.add_statement(a)

    with pytest.raises(RuntimeError):
        IntersectsWith(a, b).compile(vars)