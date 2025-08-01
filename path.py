# edge(a, b). edge(b, c). edge(c, d). edge(d, a).
# path(X, Y) :- edge(X, Y).
# path(X, Y) :- edge(X, Z), path(Z, Y).
# path(X, Y)?

from datalog import Engine
from unify import App, Const, Var

db = Engine()

# edge(a, b). edge(b, c). edge(c, d). edge(d, a).
db.assert_simple(App('edge', [Const('a'), Const('b')]))
db.assert_simple(App('edge', [Const('b'), Const('c')]))
db.assert_simple(App('edge', [Const('c'), Const('d')]))
db.assert_simple(App('edge', [Const('d'), Const('a')]))

# path(X, Y) :- edge(X, Y).
db.assert_simple(
    App('path', [Var('X'), Var('Y')]),
    App('edge', [Var('X'), Var('Y')])
)

# path(X, Y) :- edge(X, Z), path(Z, Y).
db.assert_simple(
    App('path', [Var('X'), Var('Y')]),
    App('edge', [Var('X'), Var('Z')]),
    App('path', [Var('Z'), Var('Y')])
)

# path(X, Y)?
for answer in db.ask(App('path', [Var('X'), Var('Y')])):
    print(f"{answer}.")
