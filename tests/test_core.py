import sys

from io import StringIO
import pytest
from trailrunner import core
import types


def test_process_args_dry_run_prints_command(monkeypatch):
    def fake_load_data(args):
        return (["psql", "-f", args.file], None)

    monkeypatch.setattr(core, "load_data", fake_load_data)

    buf, old = StringIO(), sys.stdout
    sys.stdout = buf
    try:
        return_code = core.process_args(create_args(dry_run=True))
    finally:
        sys.stdout = old

    stdout = buf.getvalue()
    assert "psql" in stdout
    assert return_code is None


def test_process_args_success(monkeypatch):
    monkeypatch.setattr(core, "show_progress", lambda progress: None)

    class FakeProc:
        returncode = 0

        def communicate(self):
            return ("ok", "")

        def poll(self):
            return 0

    def fake_load_data(args):
        return (["psql", ""], FakeProc())

    monkeypatch.setattr(core, "load_data", fake_load_data)

    return_code = core.process_args(create_args())
    assert return_code is None


def test_process_args_failure_raises_with_stderr(monkeypatch):
    from trailrunner.error import RunError

    monkeypatch.setattr(core, "show_progress", lambda progress: None)
    stderr_msg = "error"

    class FakeProc:
        returncode = 2

        def communicate(self):
            return ("", stderr_msg)

        def poll(self):
            return 0

    def fake_load_data(args):
        return (["psql", "--flag", ""], FakeProc())

    monkeypatch.setattr(core, "load_data", fake_load_data)

    with pytest.raises(RunError) as e:
        core.process_args(create_args())

    err_msg = str(e.value)
    assert "return code 2" in err_msg
    assert stderr_msg in err_msg


def create_args(**data):
    Args = types.SimpleNamespace
    arg_map = dict(file="/tmp/a.sql",
                   host="localhost",
                   port="5432",
                   user="u",
                   dbname="pawx",
                   prompt_password=False,
                   dry_run=False)
    arg_map.update(data)
    return Args(**arg_map)