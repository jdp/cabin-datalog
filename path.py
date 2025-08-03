# edge(a, b). edge(b, c). edge(c, d). edge(d, a).
# path(X, Y) :- edge(X, Y).
# path(X, Y) :- edge(X, Z), path(Z, Y).
# path(X, Y)?

from datalog import Engine
from unify import Atom, Const, Var

db = Engine()

# edge(a, b). edge(b, c). edge(c, d). edge(d, a).
db.assert_simple(Atom('edge', [Const('a'), Const('b')]))
db.assert_simple(Atom('edge', [Const('b'), Const('c')]))
db.assert_simple(Atom('edge', [Const('c'), Const('d')]))
db.assert_simple(Atom('edge', [Const('d'), Const('a')]))

# path(X, Y) :- edge(X, Y).
db.assert_simple(
    Atom('path', [Var('X'), Var('Y')]),
    Atom('edge', [Var('X'), Var('Y')])
)

# path(X, Y) :- edge(X, Z), path(Z, Y).
db.assert_simple(
    Atom('path', [Var('X'), Var('Y')]),
    Atom('edge', [Var('X'), Var('Z')]),
    Atom('path', [Var('Z'), Var('Y')])
)

# path(X, Y)?
for answer in db.ask(Atom('path', [Var('X'), Var('Y')])):
    print(f"{answer}.")
