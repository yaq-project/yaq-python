__all__ = ["FakeTriggeredSensor"]


import asyncio
import random

from yaqd_core import HasMeasureTrigger, IsSensor, IsDaemon


def random_walk(min_, max_):
    # A random walk with weight. Will be held to the center of the dynamic range.
    center = (max_ + min_) / 2
    width = (max_ - min_) * 10
    val = center
    while True:
        yield val
        step = random.gauss(mu=0, sigma=(max_ - min_) / 25)
        step += (center - val) / width
        val += step
        # clip
        val = max(val, min_)
        val = min(val, max_)


class FakeTriggeredSensor(HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "fake-triggered-sensor"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # populate channels
        self._channel_names = []
        self._channel_units = {}
        self._channel_shapes = {}
        self._channel_generators = {}  # unique to this daemon
        for name, kwargs in self._config["channels"].items():
            self._channel_names.append(name)
            self._channel_units[name] = None
            self._channel_shapes[name] = kwargs.get("shape", ())
            if kwargs["kind"] == "random-walk":
                min_ = self._config["channels"][name]["min"]
                max_ = self._config["channels"][name]["max"]
                self._channel_generators[name] = random_walk(min_, max_)
            else:
                raise Exception(f"channel kind {kwargs['kind']} not recognized")

    async def _measure(self):
        out = {}
        for name in self._channel_names:
            out[name] = next(self._channel_generators[name])
        if self._looping:
            await asyncio.sleep(0.1)
        return out
