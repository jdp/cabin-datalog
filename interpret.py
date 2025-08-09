from evaluate import evaluate_naive
from expr import Atom, Const, Rule, Var
from commands import Assertion, Query


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

    def run(self, program):
        for node in program:
            match node:
                case Assertion():
                    self.assert_rule(node.rule)
                case Query():
                    yield from self.ask(node.atom)


def eval_program(program):
    dl = Engine()
    return dl.run(program)


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
