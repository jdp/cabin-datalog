from itertools import product

from database import Database
from expr import Assertion, Atom, Const, Query, Rule, Var
from unify import substitute


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


def eval_program(program, dl=None):
    if dl is None:
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
