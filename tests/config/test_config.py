import pathlib
import shutil
import subprocess
import sys

import appdirs
import pytest
import toml

import yaqc
from yaqd_core import testing

here = pathlib.Path(__file__).parent


def test_malformed():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(
            [
                sys.executable,
                here / "config.py",
                "--config",
                here / "malformed.toml",
            ],
            check=True,
            timeout=0.5,
        )


def test_log():
    directory = pathlib.Path(appdirs.user_log_dir("yaqd-config-test", "yaqd"))
    try:
        assert not directory.exists()
        with pytest.raises(subprocess.TimeoutExpired):
            subprocess.run(
                [
                    sys.executable,
                    here / "config.py",
                    "--config",
                    here / "log.toml",
                ],
                check=True,
                capture_output=True,
                timeout=0.3,
            )
        assert directory.exists()
    finally:
        shutil.rmtree(directory)


@testing.run_daemon_from_file(here / "config.py", here / "types.toml")
def test_types():
    d = yaqc.Client(39999)
    assert toml.loads(d.get_config())["test"] == d.get_test()
    assert toml.loads(d.get_config())["test"] == {"name": "types", "value": 0}
    assert toml.loads(d.get_config())["nested"]["lo"]["test"] == {
        "name": "hi",
        "value": 0,
    }
