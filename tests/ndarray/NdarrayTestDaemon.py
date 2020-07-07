import yaqd_core
import numpy as np


class NdarrayTestDaemon(yaqd_core.Base):
    _kind = "ndarray-test"

    def subtract(self, minuend, subtrahend):
        return minuend - subtrahend

    def sum(self, arr):
        return np.sum(arr)


if __name__ == "__main__":
    NdarrayTestDaemon.main()
