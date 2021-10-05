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


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_set_position():
    c = yaqc.Client(39424)
    c.set_position(0)
    while c.busy():
        time.sleep(0.01)
    assert math.isclose(c.get_position(), 0)
    c.set_position(1)
    while c.busy():
        time.sleep(0.01)
    assert math.isclose(c.get_position(), 1)


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_units_set():
    c = yaqc.Client(39424)
    assert c.get_units() == "mm"


@testing.run_daemon_entry_point("fake-continuous-hardware", config=config)
def test_properties():
    c = yaqc.Client(39424)
    c.set_position(0.33)
    while c.busy():
        time.sleep(0.01)
    assert "position" in c.properties
    assert math.isclose(c.properties.position(), 0.33)
    assert c.properties.position.units() == "mm"
    assert c.properties.position.control_kind == "hinted"
    assert c.properties.position.record_kind == "data"
    assert c.properties.position.type == "double"
    assert c.properties.position.limits() == [0.0, 1.0]
    assert "destination" in c.properties
    assert math.isclose(c.properties.destination(), 0.33)
    assert c.properties.destination.units() == "mm"
    assert c.properties.destination.control_kind == "normal"
    assert c.properties.destination.record_kind == "data"
    assert c.properties.destination.type == "double"


if __name__ == "__main__":
    test_set_position()
    test_units_set()
