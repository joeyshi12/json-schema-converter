from enum import Enum
from dataclasses import dataclass


class DataType(Enum):
    BOOLEAN = 1
    INTEGER = 2
    STRING = 3
    DATE = 4


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
