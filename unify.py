# https://eli.thegreenplace.net/2018/unification/

class Term:
    @property
    def is_ground(self):
        return False


class App(Term):
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


def unify(x, y, subst):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif isinstance(x, Var):
        return unify_variable(x, y, subst)
    elif isinstance(y, Var):
        return unify_variable(y, x, subst)
    elif isinstance(x, App) and isinstance(y, App):
        if x.fname != y.fname or len(x.args) != len(y.args):
            return None
        else:
            for i in range(len(x.args)):
                subst = unify(x.args[i], y.args[i], subst)
            return subst
    else:
        return None


def unify_variable(v, x, subst):
    assert isinstance(v, Var)
    if v.name in subst:
        return unify(subst[v.name], x, subst)
    elif isinstance(x, Var) and x.name in subst:
        return unify(v, subst[x.name], subst)
    elif occurs_check(v, x, subst):
        return None
    else:
        return {**subst, v.name: x}


def occurs_check(v, term, subs):
    assert isinstance(v, Var)
    if v == term:
        return True
    elif isinstance(term, Var) and term.name in subs:
        return occurs_check(v, subs[term.name], subs)
    elif isinstance(term, App):
        return any(occurs_check(v, arg, subs) for arg in term.args)
    else:
        return False
