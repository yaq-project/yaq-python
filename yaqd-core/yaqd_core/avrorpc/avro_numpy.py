import fastavro  # type: ignore


class Interface:
    def __init__(self, array_interface):
        array_interface["shape"] = tuple(array_interface["shape"])
        self.__array_interface__ = array_interface


def read_ndarray(data, writer_schema, reader_schema):
    import numpy as np  # type: ignore

    return np.array(Interface(data))


def prepare_ndarray(data, schema):
    if hasattr(data, "__array_interface__"):
        array_interface = data.__array_interface__.copy()
        array_interface["data"] = data.tobytes()
        array_interface["shape"] = list(array_interface["shape"])
        return array_interface
    else:
        return data


fastavro.read.LOGICAL_READERS["record-ndarray"] = read_ndarray
fastavro.write.LOGICAL_WRITERS["record-ndarray"] = prepare_ndarray
