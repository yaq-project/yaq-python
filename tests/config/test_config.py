import pathlib
import shutil
import subprocess
import sys

import appdirs
import pytest

here = pathlib.Path(__file__).parent


def test_malformed():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(
            [sys.executable, here / "config.py", "--config", here / "malformed.toml",],
            check=True,
            timeout=0.5,
        )


def test_log():
    directory = pathlib.Path(appdirs.user_log_dir("yaqd-config-test", "yaqd"))
    try:
        assert not directory.exists()
        with pytest.raises(subprocess.TimeoutExpired):
            subprocess.run(
                [sys.executable, here / "config.py", "--config", here / "log.toml",],
                check=True,
                capture_output=True,
                timeout=0.2,
            )
        assert directory.exists()
    finally:
        shutil.rmtree(directory)
