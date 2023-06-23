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


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_transform():
    c = yaqc.Client(38001)
    c.set_native_reference(1.0)
    val=3.0
    assert np.isclose(c.to_native(val),2.5)
    bb=c.to_transformed(c.to_native(val))
    assert np.isclose(val,bb)


@testing.run_daemon_entry_point("fake-has-transformed-position", config=config)
def test_limits():
    c = yaqc.Client(38001)
    val=3.0
    c.set_position(val)
    time.sleep(0.10)
    assert np.isclose(c.get_position(),val)

    val=0.5
    c.set_position(val)
    time.sleep(0.10)
    assert np.isclose(c.get_position(),1.0)

    val=4.5
    c.set_position(val)
    time.sleep(0.10)
    assert np.isclose(c.get_position(),4.0)

    lims1=c.get_limits()
    lims2=c.get_native_limits()
    A=[c.to_transformed(lims2[0]),c.to_transformed(lims2[1])]
    assert np.isclose(lims1[0],1.0)
    assert np.isclose(lims1[1],4.0)
    assert np.isclose(lims1[0],A[0])
    assert np.isclose(lims1[1],A[1])



