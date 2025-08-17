import argparse
import sys

from interpret import Engine
from parse import ParseFailure, parse_program


def run(dl, program):
    for answer in dl.run(program):
        print(f"{answer}.")


def run_file(dl, file):
    try:
        program = parse_program(file.read())
    except ParseFailure:
        sys.stderr.write(f"file: {file.name}: parse error\n")
        sys.exit(1)
    run(dl, program)


def run_eval(dl, commands):
    try:
        program = parse_program(commands)
    except ParseFailure:
        sys.stderr.write("eval: parse error\n")
        sys.exit(2)
    run(dl, program)


def run_repl(dl):
    while True:
        try:
            line = input("> ")
            program = parse_program(line)
        except EOFError:
            print()
            break
        except KeyboardInterrupt:
            print()
            continue
        except ParseFailure:
            sys.stderr.write("parse error\n")
            continue
        run(dl, program)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='?', type=argparse.FileType('r'))
    ap.add_argument('-e', '--eval')
    ap.add_argument('-i', '--interactive', action='store_true', default=False)
    args = ap.parse_args()
    if args.file or args.eval or args.interactive:
        dl = Engine()
        if args.file:
            run_file(dl, args.file)
        if args.eval:
            run_eval(dl, args.eval)
        if args.interactive:
            run_repl(dl)
    else:
        ap.print_usage()
