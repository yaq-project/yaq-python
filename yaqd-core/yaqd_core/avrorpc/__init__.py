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
        schema = fastavro.parse_schema(
            schema, expand=True, _named_schemas=named_types
        )

    try:
        # Needed twice for nested types... Should likely be fixed upstream
        schema = fastavro.parse_schema(
            schema, expand=True, _named_schemas=named_types
        )
    except fastavro.schema.SchemaParseException:
        pass  # Must not have needed the second pass...

    s = BytesIO()
    fastavro.schemaless_writer(s, schema, partial)
    s.seek(0)
    return fastavro.schemaless_reader(s, schema)
