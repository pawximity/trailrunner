from getpass import getpass
import os
import shutil
import subprocess

from trailrunner.config import RunError


def load_data(args):
    """Loads arg data into a psql command.

    Builds a command and spawns a subprocess unless dry_run is set.
    Returns the command and the process object. Raises an error if 
    psql isn't found on the class path.
    """
    if not shutil.which("psql"):
        raise RunError(
            "psql not found in PATH. Make sure postgresql-client is installed")
    command = build_command(args)
    if args.dry_run:
        return command, None
    env_copy = os.environ.copy()
    if args.prompt_password:
        env_copy["PGPASSWORD"] = getpass("[!] Postgres password ")
    process = subprocess.Popen(command,
                               env=env_copy,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               text=True)
    return command, process


def build_command(args):
    command = [
        "psql",
        "-h",
        args.host,
        "-p",
        args.port,
        "-U",
        args.user,
        "-d",
        args.dbname,
        "-v",
        "ON_ERROR_STOP=1",
        "--single-transaction",
        "--no-psqlrc",
        "--pset",
        "pager=off",
        "--echo-errors",
        "-c",
        "SET application_name = 'trailrunner';",
        "-c",
        "SET client_min_messages = WARNING;",
        "-c",
        "SET statement_timeout = '30min';",
        "-c",
        "SET lock_timeout = '0';",
        "-c",
        "SET work_mem = '256MB';",
        "-c",
        "SET maintenance_work_mem = '512MB';",
        "-c",
        "SET jit = off;",
        "-f",
        args.file,
    ]
    return command