import yaqd_core
import numpy as np


class NdarrayTestDaemon(yaqd_core.Base):
    _kind = "ndarray-test"

    def subtract(self, minuend, subtrahend):
        return minuend - subtrahend

    def sum(self, arr):
        return np.sum(arr)

    def shape(self):
        return np.linspace(0, 1, 10).reshape(2, 5)

    def union(self):
        return np.linspace(0, 1, 10).reshape(2, 5)

    def map_union(self):
        return {
            "simple": np.linspace(0, 1, 10),
            "complicated": np.linspace(0, 1, 10).reshape(2, 5),
        }


if __name__ == "__main__":
    NdarrayTestDaemon.main()
