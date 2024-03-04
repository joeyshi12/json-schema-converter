import re
from typing import Optional
from jdtt.schema import Schema, SchemaField, SchemaBasicDataType, \
        SchemaDataType, SchemaListDataType, SchemaReference, DataType
from jdtt.transcompilation import schemas_to_python, schemas_to_scala, \
        schemas_to_typescript


def transcompile(schema_json: dict,
                 target_language: str = "python",
                 date_format: Optional[str] = None,
                 schema_name: str = "Schema") -> str:
    schema_dict = json_to_schemas(schema_json, date_format, schema_name)
    match target_language:
        case "python":
            return schemas_to_python(schema_dict)
        case "scala":
            return schemas_to_scala(schema_dict)
        case "typescript":
            return schemas_to_typescript(schema_dict)
        case _:
            raise Exception("Invalid target language " + target_language)


def json_to_schemas(schema_json: dict,
                    date_format: Optional[str] = None,
                    schema_name: str = "Schema") -> dict[str, Schema]:
    """Infers a language data type schema from the given JSON object."""
    return _json_to_schemas(schema_name, schema_json, {}, date_format)


def _json_to_schemas(name: str,
                     schema_json,
                     schema_dict: dict[str, Schema],
                     date_format: Optional[str] = None) -> dict[str, Schema]:
    if not isinstance(schema_json, dict) or name in schema_dict:
        return schema_dict
    schema = Schema(name, [])
    schema_dict[name] = schema
    for member, mvalue in schema_json.items():
        schema_type = _get_or_create_schema_type(member, mvalue, schema_dict, date_format)
        schema.fields.append(SchemaField(member, schema_type))
    return schema_dict


def _get_or_create_schema_type(member: str,
                               mvalue,
                               schema_dict: dict[str, Schema],
                               date_format: Optional[str] = None) -> SchemaDataType:
    """Returns the type of a member, creating a new schema if necessary."""
    match mvalue:
        case str() if date_format is not None and re.match(date_format, mvalue):
            return SchemaBasicDataType(DataType.DATE)
        case bool():
            return SchemaBasicDataType(DataType.BOOLEAN)
        case int():
            return SchemaBasicDataType(DataType.INTEGER)
        case str():
            return SchemaBasicDataType(DataType.STRING)
        case _ if mvalue is None :
            return SchemaBasicDataType(DataType.STRING)
        case list() if len(mvalue) == 0:
            return SchemaBasicDataType(DataType.STRING)
        case list():
            item_name = member + "Item"
            count = 1
            while item_name in schema_dict:
                item_name = member + "Item" + str(count)
                count += 1
            schema_item = mvalue[0]
            item_type = _get_or_create_schema_type(item_name, schema_item, schema_dict, date_format)
            return SchemaListDataType(item_type)
        case _:
            _json_to_schemas(member, mvalue, schema_dict, date_format)
            return SchemaReference(member)
