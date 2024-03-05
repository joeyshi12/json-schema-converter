from enum import Enum
from dataclasses import dataclass


class DataType(Enum):
    BOOLEAN = 1
    INTEGER = 2
    FLOAT = 3
    STRING = 4
    DATE = 5
    UNKNOWN = 6


class SchemaDataType:
    pass


@dataclass
class SchemaBasicDataType(SchemaDataType):
    data_type: DataType


@dataclass
class SchemaListDataType(SchemaDataType):
    item_type: SchemaDataType


@dataclass
class SchemaReference(SchemaDataType):
    schema_name: str


@dataclass
class SchemaField:
    name: str
    data_type: SchemaDataType


@dataclass
class Schema:
    name: str
    fields: list[SchemaField]
