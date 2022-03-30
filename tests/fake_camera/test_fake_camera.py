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


@testing.run_daemon_entry_point("fake-camera", config=config)
def test_keys():
    c = yaqc.Client(39446)
    c.measure()
    while c.busy():
        time.sleep(0.01)
    assert "image" in c.get_measured()
    assert "measurement_id" in c.get_measured()
    assert "mapping_id" in c.get_measured()
    assert "image" in c.get_channel_mappings()
    assert "x_index" in c.get_mappings()
    assert "y_index" in c.get_mappings()


@testing.run_daemon_entry_point("fake-camera", config=config)
def test_shapes():
    c = yaqc.Client(39446)
    c.measure()
    while c.busy():
        time.sleep(0.01)
    assert c.get_measured()["image"].shape == (256, 512)
    assert c.get_mappings()["x_index"].shape == (1, 512)
    assert c.get_mappings()["y_index"].shape == (256, 1)


if __name__ == "__main__":
    test_keys()
    test_shapes()
