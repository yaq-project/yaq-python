"""Class representing single property, see YEP-111."""


Getter = object()


class Property:
    def __init__(self, client, prop):
        self._client = client
        self._property = prop

        for k in ("units", "options", "limits"):
            if prop[f"{k}_getter"] is not None:
                setattr(self, k, getattr(self._client, self._property[f"{k}_getter"]))

    def __call__(self, val=Getter):
        if val is Getter:
            return getattr(self._client, self._property["getter"])()
        if not self._property["setter"]:
            raise TypeError("Property is not settable")
        return getattr(self._client, self._property["setter"])(val)

    @property
    def control_kind(self):
        return self._property["control_kind"]

    @property
    def record_kind(self):
        return self._property["record_kind"]

    @property
    def dynamic(self):
        return self._property["dynamic"]

    @property
    def type(self):
        return self._property["type"]
