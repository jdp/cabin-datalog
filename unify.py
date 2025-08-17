# https://eli.thegreenplace.net/2018/unification/

from expr import Atom, Var


def unify(x, y, subst):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif isinstance(x, Var):
        return unify_variable(x, y, subst)
    elif isinstance(y, Var):
        return unify_variable(y, x, subst)
    elif isinstance(x, Atom) and isinstance(y, Atom):
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
    elif isinstance(term, Atom):
        return any(occurs_check(v, arg, subs) for arg in term.args)
    else:
        return False
