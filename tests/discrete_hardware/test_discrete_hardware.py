import pathlib
import subprocess
import sys
import time
import math

import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_set_identifier():
    c = yaqc.Client(39425)
    for k, v in c.get_position_identifiers().items():
        c.set_identifier(k)
        time.sleep(0.1)
        assert c.get_identifier() == k


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_units_set():
    c = yaqc.Client(39425)
    assert c.get_units() == "deg"
