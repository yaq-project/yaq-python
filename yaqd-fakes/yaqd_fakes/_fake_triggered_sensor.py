__all__ = ["FakeTriggeredSensor"]


import asyncio
import random

from yaqd_core import HasMeasureTrigger, IsSensor, IsDaemon


class FakeTriggeredSensor(HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "fake-triggered-sensor"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # populate channels
        self._channel_names = []
        self._channel_units = {}
        self._channel_kinds = {}  # unique to this daemon
        for channel_name, kwargs in self._config["channels"].items():
            self._channel_names.append(channel_name)
            self._channel_units[channel_name] = None
            self._channel_kinds[channel_name] = kwargs["kind"]

    async def _measure(self):
        out = {}
        for name in self._channel_names:
            kind = self._channel_kinds[name]
            if kind == "random-walk":
                min_ = self._config["channels"][name]["min"]
                max_ = self._config["channels"][name]["max"]
                old = self._measured.get("name", (max_ + min_) / 2)
                diff = random.gauss(mu=0, sigma=(max_ - min_) / 10)
                out[name] = old + diff
            else:
                raise KeyError(f"{kind} is not a valid channel kind")
        if self._looping:
            await asyncio.sleep(0.1)
        return out
