import pytest
from trailrunner import loader
import types


def test_load_data_ogr2ogr_missing_raises(monkeypatch):
    from trailrunner.error import RunError

    monkeypatch.setattr(loader.shutil, "which", lambda *_: None)

    with pytest.raises(RunError):
        loader.load_data(create_args())


def test_load_data_dry_run(monkeypatch):
    monkeypatch.setattr(loader.shutil, "which", lambda *_: "/usr/bin/psql")

    cmd, proc = loader.load_data(create_args(dry_run=True))
    assert proc is None
    assert cmd[0] == "psql"


def test_load_data_spawns_process(monkeypatch):
    monkeypatch.setattr(loader.shutil, "which", lambda *_: "/usr/bin/psql")
    monkeypatch.setattr(loader, "getpass", lambda prompt="": "secret")

    class FakeProc:

        def __init__(self, *a, **k):
            self.returncode = None

        def poll(self):
            return None

        def communicate(self):
            return ("", "")

    seen = {}

    def fake_popen(cmd, **kw):
        seen["cmd"] = cmd
        return FakeProc()

    monkeypatch.setattr(loader.subprocess, "Popen", fake_popen)

    cmd, proc = loader.load_data(create_args())
    assert proc is not None
    assert seen["cmd"][0] == "psql"


def test_build_command_flags():
    args = create_args()
    cmd = loader.build_command(args)
    cmd_output = " ".join(cmd)
    assert cmd[0] == "psql"
    assert f"-f {args.file}" in cmd_output 
    assert f"-h {args.host}" in cmd_output
    assert f"-p {args.port}" in cmd_output 
    assert f"-U {args.user}" in cmd_output
    assert f"-d {args.dbname}" in cmd_output


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