import pathlib
import shutil
import subprocess
import sys

import appdirs
import pytest
import tomli

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
            timeout=5,
        )


def test_log():
    def rmtree(dir):
        try:
            shutil.rmtree(directory)
        except FileNotFoundError:
            pass

    directory = pathlib.Path(appdirs.user_log_dir("yaqd-config-test", "yaq"))
    rmtree(directory)
    assert not directory.exists()

    @testing.run_daemon_from_file(here / "config.py", here / "log.toml")
    def inner():
        yaqc.Client(39999)  # somehow this is needed  ---Blaise 2021-02-04
        assert directory.exists()

    inner()
    rmtree(directory)


@testing.run_daemon_from_file(here / "config.py", here / "types.toml")
def test_types():
    d = yaqc.Client(39999)
    assert tomli.loads(d.get_config())["test"] == d.get_test()
    assert tomli.loads(d.get_config())["test"] == {"name": "types", "value": 0}
    assert tomli.loads(d.get_config())["nested"]["lo"]["test"] == {
        "name": "hi",
        "value": 0,
    }


if __name__ == "__main__":
    test_malformed()
