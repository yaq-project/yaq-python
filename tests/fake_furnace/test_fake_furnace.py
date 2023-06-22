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


@testing.run_daemon_entry_point("fake-furnace", config=config)
def test_ramp():
    c = yaqc.Client(39426)
    c.set_ramp_time(0)
    c.set_position(0)
    time.sleep(1)
    assert c.get_position() == 0
    c.set_ramp_time(1)
    c.set_position(100)
    a = c.get_position()
    time.sleep(1)
    b = c.get_position()
    time.sleep(1)
    c = c.get_position()
    assert a < b < c


@testing.run_daemon_entry_point("fake-furnace", config=config)
def test_set_ramp_time():
    c = yaqc.Client(39426)
    c.properties["ramp_time"](6.22)
    assert c.properties["ramp_time"]() == 6.22


@testing.run_daemon_entry_point("fake-furnace", config=config)
def test_set_temperature():
    c = yaqc.Client(39426)
    c.set_ramp_time(0)
    c.set_position(0)
    time.sleep(1)
    assert c.get_position() == 0
    c.set_position(111)
    time.sleep(1)
    assert c.get_position() == 111
