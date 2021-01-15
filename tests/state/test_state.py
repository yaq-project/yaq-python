import os
import pathlib
import shutil
import subprocess
import sys
import time

import appdirs
import pytest
import toml

import yaqc
from yaqd_core import testing

here = pathlib.Path(__file__).parent


@testing.run_daemon_from_file(here / "state.py", here / "config.toml")
def test_update_without_busy_toggle():
    """
    In a prior implementation, the state file was only written to disk while busy is True.
    Since certain daemons are never busy, this leads to confusing behavior.
    This test protects against this.
    """
    c = yaqc.Client(39_999)
    fp = (
        pathlib.Path(appdirs.user_data_dir("yaqd-state", "yaq"))
        / "state-test"
        / "state-state.toml"
    )
    # before
    with open(fp, "r") as f:
        from_file = toml.load(f)
    from_daemon = toml.loads(c.get_state())
    assert from_file == from_daemon
    # after
    c.increment_test()
    time.sleep(2)
    with open(fp, "r") as f:
        from_file = toml.load(f)
    from_daemon = toml.loads(c.get_state())
    assert from_file == from_daemon


def test_read_at_startup():
    fp = (
        pathlib.Path(appdirs.user_data_dir("yaqd-state", "yaq"))
        / "state-test"
        / "state-state.toml"
    )
    state = {"test": -420}
    if fp.is_file():
        os.remove(fp)
    fp.parent.mkdir(parents=True, exist_ok=True)
    with open(fp, "w") as f:
        toml.dump(state, f)

    @testing.run_daemon_from_file(here / "state.py", here / "config.toml")
    def inner():
        c = yaqc.Client(39_999)
        assert toml.loads(c.get_state()) == state

    inner()


if __name__ == "__main__":
    test_update_without_busy_toggle()
    test_read_at_startup()
