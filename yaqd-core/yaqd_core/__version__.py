"""Define version."""


import pathlib
import subprocess


here = pathlib.Path(__file__).resolve().parent

__all__ = ["__version__", "__branch__", "__avro_version__"]

__avro_version__ = "1.9.2"

__version__ = "2023.11.0"

try:
    __branch__ = (
        subprocess.run(
            ["git", "branch", "--show-current"], capture_output=True, cwd=here
        )
        .stdout.strip()
        .decode()
    )
except:
    __branch__ = ""

if __branch__:
    __version__ += "+" + __branch__
