from collections import defaultdict
from itertools import chain, product

from unify import Atom, Var, Const, unify


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


class Rule:
    def __init__(self, head, body=None):
        self.head = head
        self.body = () if body is None else tuple(body)

    def __str__(self):
        if self.is_fact:
            return str(self.head)
        else:
            return f'{self.head} :- {", ".join(str(b) for b in self.body)}'

    __repr__ = __str__

    @property
    def is_fact(self):
        return self.head.is_ground and len(self.body) == 0

    @property
    def is_safe(self):
        return self.head_variables & self.body_variables == self.head_variables

    @property
    def head_variables(self):
        return set(v for v in self.head.args if isinstance(v, Var))

    @property
    def body_variables(self):
        body_args = chain.from_iterable(b.args for b in self.body)
        return set(v for v in body_args if isinstance(v, Var))


def substitute(atom, bindings):
    args = tuple(bindings[a.name] if isinstance(a, Var) else a for a in atom.args)
    return Atom(atom.fname, args)


def immediate_consequence(rules, db):
    db2 = db.copy()
    for rule in rules:
        if rule.is_fact:
            continue
        for values in product(db.constants, repeat=len(rule.body_variables)):
            binding = dict(zip([v.name for v in rule.body_variables], values))
            bound = [substitute(atom, binding) for atom in rule.body]
            if all(atom.is_ground and atom in db for atom in bound):
                derived = substitute(rule.head, binding)
                db2.add(derived)
    return db2


def evaluate_naive(rules):
    "Evaluate the rules using the naïve algorithm."
    db = Database()
    for rule in rules:
        if rule.is_fact:
            db.add(rule.head)
    while True:
        db2 = immediate_consequence(rules, db)
        if db == db2:
            break
        else:
            db = db2
    return db


class Assertion:
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return f"{self.rule}."

    __repr__ = __str__


class Query:
    def __init__(self, atom):
        self.atom = atom

    def __str__(self):
        return f"{self.atom}?"

    __repr__ = __str__


class Engine:
    def __init__(self):
        self.rules = []

    def assert_rule(self, rule):
        assert rule.is_safe
        self.rules.append(rule)

    def assert_simple(self, head, *body):
        self.assert_rule(Rule(head, body))

    def ask(self, query):
        db = evaluate_naive(self.rules)
        yield from db.search(query)


def eval_program(program):
    dl = Engine()
    for node in program:
        match node:
            case Assertion():
                dl.assert_rule(node.rule)
            case Query():
                yield from dl.ask(node.atom)


if __name__ == '__main__':
    answers = eval_program([
        Assertion(Rule(Atom('edge', [Const('a'), Const('b')]))),
        Assertion(Rule(Atom('edge', [Const('b'), Const('c')]))),
        Assertion(Rule(Atom('edge', [Const('c'), Const('d')]))),
        Assertion(Rule(Atom('edge', [Const('d'), Const('a')]))),
        Assertion(Rule(Atom('path', [Var('X'), Var('Y')]), [
            Atom('edge', [Var('X'), Var('Y')])
        ])),
        Assertion(Rule(Atom('path', [Var('X'), Var('Y')]), [
            Atom('path', [Var('X'), Var('Z')]),
            Atom('path', [Var('Z'), Var('Y')])
        ])),
        Query(Atom('path', [Var('X'), Var('Y')]))
    ])
    for answer in answers:
        print(f"{answer}.")
