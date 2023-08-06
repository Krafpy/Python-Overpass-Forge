from __future__ import annotations

from .variables import VariableManager
from .base import Statement, QueryStatement, BlockStatement
from .variables import VariableManager


class Nodes(QueryStatement):
    _type_specifier: str = "node"

class Ways(QueryStatement):
    _type_specifier: str = "way"

class Relations(QueryStatement):
    _type_specifier: str = "rel"

class Areas(QueryStatement):
    _type_specifier: str = "area"


class Union(BlockStatement):
    def __init__(self, *elements: Statement) -> None:
        super().__init__()
        self.elements = list(elements)
    
    @property
    def dependencies(self) -> list[Statement]:
        return [*self.elements]
    
    def compile(self, vars: VariableManager, out_var: str | None = None) -> str:
        substmts = []
        for stmt in self.elements:
            substmts.append(vars.get_or_compile(stmt, ".{};"))
        if out_var is None:
            return f"({' '.join(substmts)});"
        return f"({' '.join(substmts)})->{out_var};"


class Difference(BlockStatement):
    def __init__(self, a: Statement, b: Statement) -> None:
        super().__init__()
        self.a = a
        self.b = b
    
    @property
    def dependencies(self) -> list[Statement]:
        return [self.a, self.b]
    
    def compile(self, vars: VariableManager, out_var: str | None = None) -> str:
        a = vars.get_or_compile(self.a, ".{};")
        b = vars.get_or_compile(self.b, ".{};")
        if out_var is None:
            return f"({a} - {b});"
        return f"({a} - {b})->.{out_var};"