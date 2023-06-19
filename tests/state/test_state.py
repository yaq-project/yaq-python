import os
import pathlib
import shutil
import subprocess
import sys
import time

import platformdirs
import pytest
import tomli
import tomli_w

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
        platformdirs.user_data_path("yaqd-state", "yaq")
        / "state-test"
        / "state-state.toml"
    )
    # before
    with open(fp, "rb") as f:
        from_file = tomli.load(f)
    from_daemon = tomli.loads(c.get_state())
    assert from_file == from_daemon
    # after
    c.increment_test()
    time.sleep(2)
    with open(fp, "rb") as f:
        from_file = tomli.load(f)
    from_daemon = tomli.loads(c.get_state())
    assert from_file == from_daemon


def test_read_at_startup():
    fp = (
        platformdirs.user_data_path("yaqd-state", "yaq")
        / "state-test"
        / "state-state.toml"
    )
    state = {"test": -420}
    if fp.is_file():
        os.remove(fp)
    fp.parent.mkdir(parents=True, exist_ok=True)
    with open(fp, "wb") as f:
        tomli_w.dump(state, f)

    @testing.run_daemon_from_file(here / "state.py", here / "config.toml")
    def inner():
        c = yaqc.Client(39_999)
        assert tomli.loads(c.get_state()) == state

    inner()


if __name__ == "__main__":
    test_update_without_busy_toggle()
    test_read_at_startup()
