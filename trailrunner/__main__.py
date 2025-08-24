"""
trailrunner - A lightweight CLI wrapper for psql.

This tool runs SQL scripts in Postgres with minimal overhead.

Usage:
    trailrunner --file myscript.sql --dbname pawx 
"""
import argparse

from trailrunner.core import process_args
from trailrunner.error import TrailRunnerError


def trail():
    return r"""
   /\  
  /  \    
 /    \________________
"""


def main():
    print(trail())
    parser = arg_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except TrailRunnerError as e:
        print("[!]", e)
        return 1


def arg_parser():
    parser = argparse.ArgumentParser(
        description="trailrunner: lightweight SQL script runner for Postgres")
    commands_subparser = parser.add_subparsers(title="commands",
                                               dest="command",
                                               required=True)
    run_parser = commands_subparser.add_parser(
        "run", help="run a SQL script in Postgres")
    run_parser.add_argument("--file",
                            required=True,
                            help="path to the SQL script to execute")
    run_parser.add_argument("--host",
                            default="localhost",
                            help="postgres host (default: localhost)")
    run_parser.add_argument("--port",
                            default="5432",
                            help="postgres port (default: 5432)")
    run_parser.add_argument("--user", help="postgres user")
    run_parser.add_argument("--prompt-password",
                            action="store_true",
                            help="prompt for postgres password")
    run_parser.add_argument("--dbname",
                            required=True,
                            help="postgres database")
    run_parser.add_argument("--dry-run",
                            action="store_true",
                            help="print the psql command and exit")
    run_parser.set_defaults(func=process_args)
    return parser


if __name__ == '__main__':
    raise SystemExit(main())