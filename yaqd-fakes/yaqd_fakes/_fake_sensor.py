__all__ = ["FakeSensor"]


import asyncio

from yaqd_core import IsSensor, IsDaemon

from ._signal_generators import random_walk


class FakeSensor(IsSensor, IsDaemon):
    _kind = "fake-sensor"

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
        asyncio.get_event_loop().create_task(self._update_measurements())

    async def _update_measurements(self):
        while True:
            out = {}
            for name in self._channel_names:
                out[name] = next(self._channel_generators[name])
            self._measurement_id += 1
            out["measurement_id"] = self._measurement_id
            self._measured = out
            await asyncio.sleep(self._config["update_period"])
