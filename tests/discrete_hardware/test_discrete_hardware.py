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


@testing.run_daemon_entry_point("fake-discrete-hardware", config=config)
def test_properties():
    c = yaqc.Client(39425)
    assert "position" in c.properties
    assert c.properties.position.units() == "deg"
    assert c.properties.position.control_kind == "hinted"
    assert c.properties.position.record_kind == "data"
    assert c.properties.position.type == "double"
    assert "destination" in c.properties
    assert c.properties.destination.units() == "deg"
    assert c.properties.destination.control_kind == "normal"
    assert c.properties.destination.record_kind == "data"
    assert c.properties.destination.type == "double"
    assert "position_identifier" in c.properties
    assert set(c.properties.position_identifier.options()) == {
        "red",
        "orange",
        "yellow",
        "green",
        "blue",
        "violet",
    }
    assert c.properties.position_identifier.control_kind == "hinted"
    assert c.properties.position_identifier.record_kind == "data"
    assert c.properties.position_identifier.type == "string"
