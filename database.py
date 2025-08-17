from collections import defaultdict

from expr import Atom, Const, substitute
from unify import unify


class Database:
    def __init__(self):
        self.tables = defaultdict(set)
        self.constants = set()

    def add(self, atom):
        assert atom.is_ground
        self.tables[atom.fname].add(atom)
        for term in atom.args:
            if isinstance(term, Const):
                self.constants.add(term)

    def search(self, query):
        if query.is_ground:
            if query in self.tables[query.fname]:
                yield query
        elif isinstance(query, Atom):
            for atom in self.tables[query.fname]:
                if bindings := unify(query, atom, {}):
                    yield substitute(query, bindings)

    def copy(self):
        new = type(self)()
        for k, vs in self.tables.items():
            for v in vs:
                new.tables[k].add(v)
        return new

    def __contains__(self, atom):
        if isinstance(atom, Atom):
            return atom in self.tables[atom.fname]

    def __sub__(self, other):
        db = Database()
        for k in self.tables.keys():
            db.tables[k] = self.tables[k] - other.tables[k]
        return db

    def __eq__(self, other):
        if self.tables.keys() != other.tables.keys():
            return False
        for k in self.tables.keys():
            if self.tables[k] != other.tables[k]:
                return False
        return True

    def __len__(self):
        return sum(len(v) for v in self.tables.values())
