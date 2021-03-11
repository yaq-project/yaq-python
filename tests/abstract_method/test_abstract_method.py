import pathlib
import shutil
import subprocess
import sys

import appdirs
import pytest

import yaqc
from yaqd_core import testing


here = pathlib.Path(__file__).parent


@testing.run_daemon_from_file(here / "good.py", here / "config.toml")
def test_good():
    c = yaqc.Client(39425)


def test_bad():
    with pytest.raises(Exception):
        subprocess.run(
            [
                sys.executable,
                here / "bad.py",
                "--config",
                here / "config.toml",
            ],
            check=True,
            timeout=0.5,
        )
