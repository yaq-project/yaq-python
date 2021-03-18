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


@testing.run_daemon_entry_point("fake-has-turret", config=config)
def test_set_get():
    c = yaqc.Client(39425)
    c.set_turret("visible")
    while c.busy():
        time.sleep(0.1)
    assert c.get_turret() == "visible"
