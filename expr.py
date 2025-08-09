from itertools import chain


class Term:
    @property
    def is_ground(self):
        return False


class Atom(Term):
    def __init__(self, fname, args=None):
        self.fname = fname
        self.args = () if args is None else tuple(args)

    @property
    def is_ground(self):
        return all(arg.is_ground for arg in self.args)

    def __eq__(self, other):
        return (
            type(self) is type(other)
            and self.fname == other.fname
            and len(self.args) == len(other.args)
            and all(a == b for a, b in zip(self.args, other.args))
        )

    def __str__(self):
        return f"{self.fname}({', '.join(str(arg) for arg in self.args)})"

    def __hash__(self):
        return hash(self.args)

    __repr__ = __str__


class Var(Term):
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        return type(self) is type(other) and self.name == other.name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

    __repr__ = __str__


class Const(Term):
    def __init__(self, value):
        self.value = value

    def is_ground(self):
        return True

    def __eq__(self, other):
        return type(self) is type(other) and self.value == other.value

    def __str__(self):
        return self.value

    def __hash__(self):
        return hash(self.value)

    __repr__ = __str__


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
