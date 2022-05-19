import asyncio

import numpy as np

from yaqd_core import HasMapping, HasMeasureTrigger, IsSensor, IsDaemon

from ._signal_generators import random_walk


class FakeCamera(HasMapping, HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "fake-camera"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        self.x_pos = random_walk(
            config["aoi_left"], config["aoi_left"] + config["aoi_width"]
        )
        self.y_pos = random_walk(
            config["aoi_top"], config["aoi_top"] + config["aoi_height"]
        )
        self.fwhm = random_walk(0, min(config["aoi_width"], config["aoi_height"]))
        self.amp = random_walk(0, 4096)
        self.x_index = np.arange(
            config["aoi_left"], config["aoi_left"] + config["aoi_width"], dtype="i2"
        )[None, :]
        self.y_index = np.arange(
            config["aoi_top"], config["aoi_top"] + config["aoi_height"], dtype="i2"
        )[:, None]
        # populate channels
        self._channel_names = ["image"]
        self._channel_units = {"image": None}
        self._channel_mappings = {"image": ["x_index", "y_index"]}
        self._channel_shapes = {"image": [config["aoi_height"], config["aoi_width"]]}
        self._mappings = {"x_index": self.x_index, "y_index": self.y_index}
        self.rng = np.random.default_rng()

    async def _measure(self):
        await asyncio.sleep(0.1)
        cen_x, cen_y = next(self.x_pos), next(self.y_pos)
        dist = np.sqrt((self.x_index - cen_x) ** 2 + (self.y_index - cen_y) ** 2)
        amp = next(self.amp)
        out = {}
        out["image"] = (np.sinc(dist / next(self.fwhm)) ** 2 * amp).astype("i2")
        out["image"] += np.abs(
            self.rng.normal(scale=100, size=out["image"].shape)
        ).astype("i2")
        return out
