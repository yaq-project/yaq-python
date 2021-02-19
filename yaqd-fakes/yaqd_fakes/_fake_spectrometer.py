import asyncio


from yaqd_core import HasMapping, HasMeasureTrigger, IsSensor, IsDaemon


class FakeSpectrometer(HasMapping, HasMeasureTrigger, IsSensor, IsDaemon):
    _kind = "fake-spectrometer"

    def __init__(self, name, config, config_filepath):
        super().__init__(name, config, config_filepath)
        # populate channels
        self._channel_names = ["counts"]
        self._channel_units = {"counts": None}
        self._channel_mappings = {"counts": ["wavelengths"]}
        self._mapping_units = {"wavelengths": "nm"}

    async def _measure(self):
        import numpy as np
        from numpy import random

        await asyncio.sleep(0.1)
        # mapping
        if "wavelengths" not in self._mappings or not np.isclose(
            self._mappings["wavelengths"][275], self._state["central_wavelength"]
        ):
            self._mappings["wavelengths"] = self._gen_mapping()
        # channels
        G = 3
        xi = self._mappings["wavelengths"]
        x0 = self._state["central_wavelength"]
        out = {}
        out["counts"] = G ** 2 / ((xi - x0) ** 2 + G ** 2)
        out["counts"] *= 100
        out["counts"] = np.round(out["counts"], decimals=0)
        out["counts"] += random.poisson(lam=10, size=551)
        return out

    def get_central_wavelength(self) -> float:
        return self._state["central_wavelength"]

    def set_central_wavelength(self, new: float):
        self._state["central_wavelength"] = new

    def _gen_mapping(self):
        import numpy as np

        center = self._state["central_wavelength"]
        return np.linspace(start=center + 25, stop=center - 25, num=551)
