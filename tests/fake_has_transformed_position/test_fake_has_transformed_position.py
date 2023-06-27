import pathlib
import subprocess
import sys
import time
import math
import numpy as np

import pytest

import yaqc
import yaqd_core
from yaqd_core import testing


config = pathlib.Path(__file__).parent / "config.toml"


def to_native(t, nr=1):
    #  n = 0.5*t - 1
    rel = 0.5 * t
    return rel + nr


def to_transformed(n, nr=1):
    #  t = 2*(n - 1)
    rel = n - nr
    return 2 * rel


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_transform():
    c = yaqc.Client(38001)
    c.set_native_reference(1.0)
    val = 3.0
    assert np.isclose(c.to_native(val), 2.5)
    bb = c.to_transformed(c.to_native(val))
    assert np.isclose(val, bb)


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_limits():
    c = yaqc.Client(38001)

    assert np.isclose(c.get_limits(), [1., 4.]).all()
    assert np.isclose(c.get_native_limits(), [1.5, 3]).all()

    val = 3.0
    c.set_position(val)
    time.sleep(0.10)
    assert np.isclose(c.get_position(), val)
    assert np.isclose(c.get_native_position(), to_native(val))

    val = 0.5
    c.set_position(val)
    time.sleep(0.10)
    assert np.isclose(c.get_position(), 1.0)

    val = 4.5
    c.set_position(val)
    time.sleep(0.10)
    assert np.isclose(c.get_position(), 4.0)

    lims1 = c.get_limits()
    lims2 = c.get_native_limits()
    A = [c.to_transformed(lims2[0]), c.to_transformed(lims2[1])]
    assert np.isclose(lims1[0], 1.0)
    assert np.isclose(lims1[1], 4.0)
    assert np.isclose(lims1[0], A[0])
    assert np.isclose(lims1[1], A[1])


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_change_native_reference():
    c = yaqc.Client(38001)

    t_pos = 2
    c.set_native_reference(1)
    c.set_position(t_pos)
    time.sleep(0.1)

    try:
        native_position = c.get_native_position()
        c.set_native_reference(c.get_native_reference() + 1)

        assert native_position == c.get_native_position()
        assert c.get_position() == to_transformed(to_native(t_pos) - 1)
    finally:
        c.set_native_reference(1)


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_set_relative():
    c = yaqc.Client(38001)
    print(c.get_limits())
    c.set_position(c.get_limits()[0])
    time.sleep(0.1)
    c.set_relative(1.)
    time.sleep(0.1)
    try:
        assert np.isclose(c.get_position(), 2.)
    except AssertionError as e:
        print(c.get_position())
        raise e


if __name__ == "__main__":
    # test_transform()
    # test_limits()
    # test_change_native_reference()
    # test_native_limits()
    test_set_relative()
