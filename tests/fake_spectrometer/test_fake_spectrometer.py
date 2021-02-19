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


@testing.run_daemon_entry_point("fake-spectrometer", config=config)
def test_keys():
    c = yaqc.Client(39426)
    c.measure()
    while c.busy():
        time.sleep(0.01)
    assert "counts" in c.get_measured()
    assert "measurement_id" in c.get_measured()
    assert "mapping_id" in c.get_measured()
    assert "counts" in c.get_channel_mappings()
    assert "wavelengths" in c.get_mappings()
    assert "wavelengths" in c.get_mapping_units()


@testing.run_daemon_entry_point("fake-spectrometer", config=config)
def test_shapes():
    c = yaqc.Client(39426)
    c.measure()
    while c.busy():
        time.sleep(0.01)
    assert c.get_measured()["counts"].shape == (551,)
    assert c.get_mappings()["wavelengths"].shape == (551,)


@testing.run_daemon_entry_point("fake-spectrometer", config=config)
def test_central_wavelength():
    c = yaqc.Client(39426)
    c.measure()
    while c.busy():
        time.sleep(0.01)
    # a value
    c.set_central_wavelength(400)
    c.measure()
    while c.busy():
        time.sleep(0.01)
    assert np.isclose(c.get_mappings()["wavelengths"][275], 400)
    # some other value
    c.set_central_wavelength(1300)
    c.measure()
    while c.busy():
        time.sleep(0.01)
    assert np.isclose(c.get_mappings()["wavelengths"][275], 1300)


if __name__ == "__main__":
    test_keys()
    test_shapes()
    test_central_wavelength()
