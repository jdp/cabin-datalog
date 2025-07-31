from collections import defaultdict
from itertools import chain, product

from unify import App, Var, Const, unify


class Database:
    def __init__(self, items=None):
        self.tables = defaultdict(set)
        if items is not None:
            for k, vs in items:
                for v in vs:
                    self.tables[k].add(v)

    def extend(self, atom):
        assert atom.is_ground
        self.tables[atom.fname].add(atom.args)

    def __contains__(self, value):
        if isinstance(value, App):
            return value.args in self.tables[value.fname]

    def __sub__(self, other):
        db = Database()
        for k in self.tables.keys():
            db.tables[k] = self.tables[k] - other.tables[k]
        return db

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
    db2 = Database(items=db.tables.items())
    constants = set()
    for rule in program:
        if rule.is_fact:
            for term in rule.head.args:
                if isinstance(term, Const):
                    constants.add(term)
            db2.extend(rule.head)
    for rule in program:
        if not rule.is_fact:
            for values in product(constants, repeat=len(rule.variables)):
                binding = dict(zip([v.name for v in rule.variables], values))
                bound = [substitute(atom, binding) for atom in rule.body]
                if all(atom.is_ground and atom in db for atom in bound):
                    derived = substitute(rule.head, binding)
                    db2.extend(derived)
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
            db.extend(fact.head)
        while True:
            db2 = immediate_consequence(self.facts + self.rules, db)
            delta = db2 - db
            if len(delta) == 0:
                break
            else:
                db = db2
        if subst is None:
            subst = {}
        # print(f"{literal}?")
        if literal.is_ground:
            print(literal)
        elif isinstance(literal, App):
            for args in db2.tables[literal.fname]:
                if bindings := unify(literal, App(literal.fname, args), subst):
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
