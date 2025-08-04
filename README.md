# Cabin Datalog

Cabin Datalog is a toy Datalog made to study logic programming,
unification,
query processing,
and other related concepts.

This is a work in progress. 

## Introduction to Datalog

Datalog is a declarative logic programming language,
superficially similar to Prolog,
frequently used as a database query language.

A Datalog program is a set of facts and rules.
Evaluating a program yields all the facts that satisfy those rules,
including new facts that weren't explicit but were derived from the rules.

Here's a program that finds all pairs of nodes that have a path between them:

``` datalog
edge(a, b). edge(b, c). edge(c, d). edge(d, a).
path(X, Y) :- edge(X, Y).
path(X, Y) :- edge(X, Z), path(Z, Y).
path(X, Y)?
```

## Python module usage

Interactively assert rules and query them:

``` python
d = Session()

# edge(a, b). edge(b, c). edge(c, d).
d.assert_simple(Atom('edge', [Const('a'), Const('b')]))
d.assert_simple(Atom('edge', [Const('b'), Const('c')]))
d.assert_simple(Atom('edge', [Const('c'), Const('d')]))

# path(X, Y) :- edge(X, Y).
d.assert_simple(
    Atom('path', [Var('X'), Var('Y')]),
    Atom('edge', [Var('X'), Var('Y')])
)

# path(X, Y) :- edge(X, Z), path(Z, Y).
d.assert_simple(
    Atom('path', [Var('X'), Var('Y')]),
    Atom('edge', [Var('X'), Var('Z')]),
    Atom('path', [Var('Z'), Var('Y')])
)

# path(X, Y)?
for answer in d.ask(Atom('path', [Var('X'), Var('Y')])):
    print(answer)

# edge(d, a).
d.assert_simple(Atom('edge', [Const('d'), Const('a')]))

# path(X, Y)?
for answer in d.ask(Atom('path', [Var('X'), Var('Y')])):
    print(answer)
```

Evaluate a list of commands as a program:

``` python
from datalog import Rule, Atom, Var, Const, eval_program

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
```

## Standalone usage

Begin an interactive session:

``` bash
cabin
```

Run a program from a file:

``` bash
cabin path.dl
```

Run a program passed as an argument:

``` bash
cabin -e 'edge(a,b). edge(a,c). edge(a,B)?'
```

## Influences

* Evaluation algorithms from *Datalog and Recursive Query Processing* [paper](http://blogs.evergreen.edu/sosw/files/2014/04/Green-Vol5-DBS-017.pdf)
* Unification algorithm from [Eli Bendersky's article](https://eli.thegreenplace.net/2018/unification/)
* Language syntax and some terminology from [MITRE's Datalog](https://datalog.sourceforge.net/)
* WISC's public CS 838 lecture notes for prompting me work through evaluation with pen and paper
* Module organization from *Designing Software for Ease of Extension and Contraction* [paper](https://ieeexplore.ieee.org/document/1702607)

## Learn more

datalog dot dev or AOL keyword datalog

Ask your parents before going online
