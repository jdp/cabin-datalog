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
