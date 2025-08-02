import re
from functools import partial

from datalog import Assertion, Query, Rule, App, Const, Var


def succeed(data, rest):
    return {'failed': False, 'data': data, 'rest': rest}


def fail(expected, rest):
    return {'failed': True, 'expected': expected, 'rest': rest}


class ParseFailure(Exception):
    pass


def parse(parser, source):
    result = parser(source)
    if result['failed']:
        raise ParseFailure(result)
    else:
        return result


def text(expected):
    def parser(source):
        if source.startswith(expected):
            return succeed(expected, source[len(expected):])
        else:
            return fail(expected, source)
    return parser


def regex(pattern):
    def parser(source):
        if m := re.match(r'^' + pattern, source):
            matched = m.group()
            return succeed(matched, source[len(matched):])
        else:
            return fail(pattern, source)
    return parser


def coerce(func, parser):
    def coerce_parser(source):
        result = parser(source)
        if result['failed']:
            return result
        else:
            return succeed(func(result['data']), result['rest'])
    return coerce_parser


def apply(func, parsers):
    def apply_parsers(source):
        acc_data = []
        current_source = source
        for parser in parsers:
            result = parser(current_source)
            if result['failed']:
                return result
            acc_data.append(result['data'])
            current_source = result['rest']
        return succeed(func(*acc_data), current_source)
    return apply_parsers


def one(parsers):
    def one_parser(source):
        for parser in parsers:
            result = parser(source)
            if result['failed']:
                continue
            return result
        return fail("one of", source)
    return one_parser


def rep1(parser):
    def rep1_parser(source):
        acc_data = []
        src = source
        result = parser(src)
        if result['failed']:
            return result
        acc_data.append(result['data'])
        src = result['rest']
        while True:
            result = parser(src)
            src = result['rest']
            if result['failed']:
                break
            acc_data.append(result['data'])
        return succeed(acc_data, src)
    return rep1_parser


def maybe(value, parser):
    def maybe_parser(source):
        result = parser(source)
        if result['failed']:
            return succeed(value, result['rest'])
        else:
            return result
    return maybe_parser


def rep0(parser):
    return maybe([], rep1(parser))


keep = partial(apply, lambda *data: data[0])

seq = partial(apply, lambda *data: data[-1])

collect = partial(apply, lambda *data: data)

cons = partial(apply, lambda first, rest: [first, *rest])


def skip(junk):
    def skipper(parser):
        return apply(lambda data, _: data, [parser, junk])
    return skipper


spaces = regex(r'\s*')
lexeme = skip(spaces)

identifier = lexeme(regex('[a-z]+'))
lparen = lexeme(text('('))
rparen = lexeme(text(')'))
comma = lexeme(text(','))
implies = lexeme(text(':-'))
period = lexeme(text('.'))
question = lexeme(text('?'))
punctuation = lexeme(regex(r'[.?]'))

const = coerce(Const, identifier)
var = coerce(Var, lexeme(regex('[A-Z]+')))
term = one([const, var])
terms = cons([term, rep0(seq([comma, term]))])

args = apply(lambda *rs: rs[1], [lparen, maybe([], terms), rparen])
atom = apply(App, [identifier, maybe([], args)])
atoms = cons([atom, rep0(seq([comma, atom]))])
fact = coerce(lambda head: Rule(head, []), atom)
body = seq([implies, atoms])
rule = apply(Rule, [atom, body])
assertion = coerce(Assertion, keep([one([rule, fact]), period]))
query = coerce(Query, keep([atom, question]))


def eof(source):
    if not source:
        return succeed(None, source)
    else:
        return fail("end of input", source)


program = skip(eof)(seq([spaces, rep1(one([assertion, query]))]))

if __name__ == '__main__':
    source = """
    p. p().
    p :- q. p() :- q().
    edge(a,b).
    edge(b,c).
    edge(c,d).
    edge(d,a).
    path(X,Y) :- edge(X,Y).
    path(X,Y) :- path(X,Z), path(Z,Y).
    path(X,Y)?
    """
    print(parse(program, source))
