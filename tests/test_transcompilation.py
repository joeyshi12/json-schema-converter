import os
from jdtt.transcompilation import json_to_schemas
from jdtt.schema import SchemaField, SchemaBasicDataType, \
    SchemaListDataType, SchemaReference, DataType


def test_empty():
    json_dict = {}
    schema_name = "Test"
    schema_dict = json_to_schemas(json_dict, schema_name=schema_name)
    assert len(schema_dict) == 1

    schema = schema_dict[schema_name]
    assert schema.name == schema_name
    assert len(schema.fields) == 0


def test_int_field():
    json_dict = {"num": 0}
    schema_name = "Test"
    schema_dict = json_to_schemas(json_dict, schema_name=schema_name)
    assert len(schema_dict) == 1

    schema = schema_dict[schema_name]
    assert schema.name == schema_name
    assert len(schema.fields) == 1

    field = schema.fields[0]
    assert field.name == "num"
    assert field.data_type == SchemaBasicDataType(DataType.INTEGER)


def test_date_field():
    json_dict = {"date": "2000-01-01"}
    schema_name = "Test"
    schema_dict = json_to_schemas(json_dict, schema_name=schema_name, date_format=r"\d{4}-\d{2}-\d{2}")
    assert len(schema_dict) == 1

    schema = schema_dict[schema_name]
    assert schema.name == schema_name
    assert len(schema.fields) == 1

    field = schema.fields[0]
    assert field.name == "date"
    assert field.data_type == SchemaBasicDataType(DataType.DATE)


def test_sanitization():
    json_dict = {"0-user@email": None}
    schema_name = "Test"
    schema_dict = json_to_schemas(json_dict, schema_name=schema_name, sanitize_symbols=True)
    assert len(schema_dict) == 1

    schema = schema_dict[schema_name]
    assert schema.name == schema_name
    assert len(schema.fields) == 1

    field = schema.fields[0]
    assert field.name == "_0_user_email"
    assert field.data_type == SchemaBasicDataType(DataType.UNKNOWN)


def test_multiple_fields():
    json_dict = {
        "num": 0,
        "decimal": 0.1,
        "text": "",
        "check": False,
        "nums": [0, 1, 2],
        "empty": [],
        "obj": {},
        "objs": [{}]
    }
    schema_name = "Test"
    schema_dict = json_to_schemas(json_dict, schema_name=schema_name)
    assert len(schema_dict) == 3
    assert len(schema_dict["obj"].fields) == 0
    assert len(schema_dict["objsItem"].fields) == 0

    schema = schema_dict[schema_name]
    assert schema.name == schema_name
    assert len(schema.fields) == 8

    assert schema.fields[0] == SchemaField("num", SchemaBasicDataType(DataType.INTEGER))
    assert schema.fields[1] == SchemaField("decimal", SchemaBasicDataType(DataType.FLOAT))
    assert schema.fields[2] == SchemaField("text", SchemaBasicDataType(DataType.STRING))
    assert schema.fields[3] == SchemaField("check", SchemaBasicDataType(DataType.BOOLEAN))
    assert schema.fields[4] == SchemaField("nums", SchemaListDataType(SchemaBasicDataType(DataType.INTEGER)))
    assert schema.fields[5] == SchemaField("empty", SchemaListDataType(SchemaBasicDataType(DataType.UNKNOWN)))
    assert schema.fields[6] == SchemaField("obj", SchemaReference("obj"))
    assert schema.fields[7] == SchemaField("objs", SchemaListDataType(SchemaReference("objsItem")))
