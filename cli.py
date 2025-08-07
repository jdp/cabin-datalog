import argparse
import sys

from evaluate import eval_program
from parse import ParseFailure, parse_program


def main(infile):
    try:
        program = parse_program(infile.read())
    except ParseFailure:
        sys.stderr.write("parse error\n")
        sys.exit(1)
    for answer in eval_program(program):
        print(f"{answer}.")


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('file', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = ap.parse_args()
    main(args.file)
