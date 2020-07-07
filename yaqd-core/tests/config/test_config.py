import pathlib
import subprocess
import sys

import pytest

here = pathlib.Path(__file__).parent


def test_malformed():
    with pytest.raises(subprocess.CalledProcessError):
        subprocess.run(
            [sys.executable, here / "config.py", "--config", here / "malformed.toml",],
            check=True,
            timeout=0.5,
        )
