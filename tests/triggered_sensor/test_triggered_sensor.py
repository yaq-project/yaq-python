import pathlib
import subprocess
import sys
import time
import math

# import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "config.toml"

@testing.run_daemon_entry_point("fake-triggered-sensor", config=config)
def test_defaults():
    c = yaqc.Client(39426)
    c.measure()
    while c.busy():
        time.sleep(0.1)
    out = c.get_measured()["random_walk"]
    assert -1 <= out <= 1


@testing.run_daemon_entry_point("fake-triggered-sensor", config=config)
def test_shapes():
    # get_channel_shapes returns a tuple
    # this test ensures that fastavro doesn't break
    c = yaqc.Client(39426)
    for k, v in c.get_channel_shapes().items():
        assert hasattr(v, "__iter__")


@testing.run_daemon_entry_point("fake-triggered-sensor", config=config)
def test_restart_with_loop():
    c = yaqc.Client(39426)
    c.shutdown(restart=True)
    i = 0
    while i < 1:
        c = yaqc.Client(39426)
        print("tried to connect")
        time.sleep(0.1)
        i += 1


if __name__ == "__main__":
    test_defaults()
    test_shapes()
    test_restart_with_loop()
