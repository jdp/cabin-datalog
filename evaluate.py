from itertools import product

from database import Database
from expr import substitute


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
