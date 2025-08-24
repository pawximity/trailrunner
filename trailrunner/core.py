import shlex
import sys
import time

from trailrunner.config import RunError
from trailrunner.loader import load_data


def process_args(args):
    """Processes the given args.

    Builds a psql command from the provided args, spawns the
    subprocess, and monitors its execution. Raises an error if 
    the process fails.
    """
    print(f"[*] Running {args.file} on {args.dbname}")
    command, process = load_data(args)
    command_output = shlex.join(command)
    if process is None and args.dry_run:
        print("[+]", command_output)
        return
    print("[*] Executing command")
    print("[+]", command_output)
    show_progress(process)
    _, stderr = process.communicate()
    if process.returncode == 0:
        print("[+] Run completed successfully")
        return
    else:
        print("\n[-]", command_output)
        raise RunError(
            f"psql failed with return code {process.returncode}\n\n{stderr.strip()}"
        )


def show_progress(process):
    counter, display = 0, '~' * 50
    while process.poll() is None:
        line = f"{display[:counter % len(display)]}"
        sys.stdout.write("\r\033[K" + line)
        sys.stdout.flush()
        counter += 1
        time.sleep(0.25)
    sys.stdout.write("\r\033[K")