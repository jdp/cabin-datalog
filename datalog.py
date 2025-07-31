from collections import defaultdict
from itertools import chain, product

from unify import App, Var, Const, unify


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

    def copy(self):
        new = type(self)()
        for k, vs in self.tables.items():
            for v in vs:
                new.tables[k].add(v)
        return new

    def __contains__(self, atom):
        if isinstance(atom, App):
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


class Clause:
    def __init__(self, head, body=None):
        self.head = head
        self.body = [] if body is None else body

    def __str__(self):
        if self.is_rule:
            return f'{self.head} :- {", ".join(str(b) for b in self.body)}'
        else:
            return str(self.head)

    @property
    def is_rule(self):
        return not self.is_fact

    @property
    def is_fact(self):
        return len(self.body) == 0

    @property
    def variables(self):
        terms = chain(self.head.args, chain.from_iterable(b.args for b in self.body))
        return set(v for v in terms if isinstance(v, Var))


def substitute(atom, bindings):
    return App(atom.fname, tuple(bindings[a.name] if isinstance(a, Var) else a for a in atom.args))


def immediate_consequence(program, db):
    db2 = db.copy()
    for rule in program:
        if rule.is_fact:
            continue
        for values in product(db.constants, repeat=len(rule.variables)):
            binding = dict(zip([v.name for v in rule.variables], values))
            bound = [substitute(atom, binding) for atom in rule.body]
            if all(atom.is_ground and atom in db for atom in bound):
                derived = substitute(rule.head, binding)
                db2.add(derived)
    return db2


class Engine:
    def __init__(self):
        self.facts = []
        self.rules = []

    def assert_clause(self, clause):
        # print(f"{clause}.")
        if clause.is_fact:
            self.facts.append(clause)
        else:
            self.rules.append(clause)

    def assert_simple(self, head, *body):
        self.assert_clause(Clause(head, body))

    def ask(self, literal, subst=None):
        db = Database()
        for fact in self.facts:
            db.add(fact.head)
        while True:
            db2 = immediate_consequence(self.rules, db)
            if db == db2:
                break
            else:
                db = db2
        if subst is None:
            subst = {}
        # print(f"{literal}?")
        if literal.is_ground:
            print(literal)
        elif isinstance(literal, App):
            for atom in db2.tables[literal.fname]:
                if bindings := unify(literal, atom, subst):
                    print(f"{substitute(literal, bindings)}.")


if __name__ == '__main__':
    db = Engine()

    # species(nidoking).
    # learns(nidoking, icebeam).
    # learns(Species, icebeam)?
    db.assert_clause(Clause(App('species', [Const('nidoking')])))
    db.assert_clause(Clause(App('learns', [Const('nidoking'), Const('icebeam')])))
    db.ask(App('learns', [Var('Species'), Const('icebeam')]))

    # ancestor(A, B) :- parent(A, B)
    # ancestor(A, B) :- parent(A, C), ancestor(C, B).
    db.assert_clause(Clause(
        App('ancestor', [Var('A'), Var('B')]),
        [App('parent', [Var('A'), Var('B')])]
    ))
    db.assert_clause(Clause(
        App('ancestor', [Var('A'), Var('B')]),
        [
            App('parent', [Var('A'), Var('C')]),
            App('ancestor', [Var('C'), Var('B')])
        ]
    ))
