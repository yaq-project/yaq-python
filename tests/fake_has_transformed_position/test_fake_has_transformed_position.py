import pathlib
import subprocess
import sys
import time
import numpy as np
import tomli

import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "config.toml"


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_transform():
    c = yaqc.Client(38001)
    c.set_native_reference(1.0)
    val = 3.0
    bb = c.to_transformed(c.to_native(val))
    assert np.isclose(val, bb)


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_limits():
    for port in [38001, 38002]:
        c = yaqc.Client(port)
        config = tomli.loads(c.get_config())

        limits = c.get_limits()
        lims2 = list(map(c.to_transformed, c.get_native_limits()))
        assert np.isclose(limits, lims2).all()

        for setpoint, actual in zip(
            [limits[0] - 0.5, 0.5 * sum(limits), limits[1] + 0.5],
            [limits[0], 0.5 * sum(limits), limits[1]],
        ):
            c.set_position(setpoint)
            time.sleep(0.10)
            assert np.isclose(c.get_position(), actual)
            assert np.isclose(c.get_destination(), actual)
            assert np.isclose(c.get_native_position(), c.to_native(actual))
            assert np.isclose(c.get_native_destination(), c.to_native(actual))


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_change_native_reference():
    for port in [38001, 38002]:
        c = yaqc.Client(port)
        factor = tomli.loads(c.get_config())["factor"]

        midrange = 0.5 * sum(c.get_limits())

        c.set_native_reference(1)
        c.set_position(midrange)
        time.sleep(0.1)
        native_position = c.get_native_position()
        assert np.isclose(native_position, c.to_native(midrange))
        c.set_native_reference(1.5)

        assert np.isclose(native_position, c.get_native_position())
        assert np.isclose(
            c.get_position(), c.to_transformed(c.to_native(midrange) - 0.5)
        )


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_set_relative():
    c = yaqc.Client(38001)
    c.set_position(c.get_limits()[0])
    initial = c.get_position()
    time.sleep(0.1)
    destination = c.set_relative(1.0)
    time.sleep(0.1)

    assert np.isclose(destination, initial + 1.0)


if __name__ == "__main__":
    test_change_native_reference()
    test_limits()
    test_set_relative()
    test_transform()
