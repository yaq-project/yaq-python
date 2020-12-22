from .unpacker import *
from . import avro_numpy

import fastavro  # type: ignore
from io import BytesIO


def fill_avro_default(schema, partial, named_types=None):
    try:
        schema = fastavro.parse_schema(
            schema["type"], expand=True, _named_schemas=named_types
        )
    except fastavro.schema.UnknownType:
        # e.g. array with flattend items types
        schema = fastavro.parse_schema(schema, expand=True, _named_schemas=named_types)

    # Sometimes fastavro.parse_schema doesn't add these like I think it should
    # One way that works with some schemas is to run it through fastavro twice.
    # However, that does not work if a map or array is the top level object.
    # Later on, when consuming the schema (read or write) it still looks for these
    # special internal behavior keys, so this just directly adds them indiscriminantly.
    # In doing so, fastavro can use the named_schemas as a lookup table whenever
    # it needs one of the named types.
    # It is still necessary to do the first pass for reasons that are not fully
    # clear, but in part because it does expand the string type name into the dict
    # in which these are placed.
    if isinstance(schema, dict):
        schema["__fastavro_parsed"] = True
        schema["__named_schemas"] = named_types

    s = BytesIO()
    fastavro.schemaless_writer(s, schema, partial)
    s.seek(0)
    return fastavro.schemaless_reader(s, schema)
