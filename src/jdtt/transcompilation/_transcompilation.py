import re
from typing import Optional
from jdtt.schema import Schema, SchemaField, SchemaBasicDataType, \
        SchemaDataType, SchemaListDataType, SchemaReference, DataType
from jdtt.transcompilation import schemas_to_python, schemas_to_typescript, \
        schemas_to_java, schemas_to_scala


def transcompile(schema_json: dict,
                 target_language: str = "python",
                 date_format: Optional[str] = None,
                 schema_name: str = "Schema",
                 sanitize_symbols: bool = False) -> str:
    schema_dict = json_to_schemas(schema_json, date_format, schema_name, sanitize_symbols)
    match target_language:
        case "python":
            return schemas_to_python(schema_dict)
        case "typescript":
            return schemas_to_typescript(schema_dict)
        case "java":
            return schemas_to_java(schema_dict)
        case "scala":
            return schemas_to_scala(schema_dict)
        case _:
            raise Exception("Invalid target language " + target_language)


def json_to_schemas(schema_json: dict,
                    date_format: Optional[str] = None,
                    schema_name: str = "Schema",
                    sanitize_symbols: bool = False) -> dict[str, Schema]:
    """Infers a language data type schema from the given JSON object."""
    return _json_to_schemas(schema_name, schema_json, {}, date_format, sanitize_symbols)


def _json_to_schemas(name: str,
                     schema_json,
                     schema_dict: dict[str, Schema],
                     date_format: Optional[str] = None,
                     sanitize_symbols: bool = False) -> dict[str, Schema]:
    if not isinstance(schema_json, dict) or name in schema_dict:
        return schema_dict
    schema = Schema(name, [])
    schema_dict[name] = schema
    for key, value in schema_json.items():
        sanitized_key = _sanitize_symbol(key) if sanitize_symbols else key
        schema_type = _get_or_create_schema_type(sanitized_key, value, schema_dict, date_format, sanitize_symbols)
        schema.fields.append(SchemaField(sanitized_key, schema_type))
    return schema_dict


def _get_or_create_schema_type(key: str,
                               value,
                               schema_dict: dict[str, Schema],
                               date_format: Optional[str] = None,
                               sanitize_symbols: bool = False) -> SchemaDataType:
    """Returns the type of the given value, creating a new schema if necessary."""
    match value:
        case str() if date_format is not None and _is_valid_date(value, date_format):
            return SchemaBasicDataType(DataType.DATE)
        case bool():
            return SchemaBasicDataType(DataType.BOOLEAN)
        case int():
            return SchemaBasicDataType(DataType.INTEGER)
        case float():
            return SchemaBasicDataType(DataType.FLOAT)
        case str():
            return SchemaBasicDataType(DataType.STRING)
        case _ if value is None :
            return SchemaBasicDataType(DataType.UNKNOWN)
        case list() if len(value) == 0:
            return SchemaListDataType(SchemaBasicDataType(DataType.UNKNOWN))
        case list():
            item_name = key + "Item"
            count = 1
            while item_name in schema_dict:
                item_name = key + "Item" + str(count)
                count += 1
            schema_item = value[0]
            item_type = _get_or_create_schema_type(item_name, schema_item, schema_dict, date_format)
            return SchemaListDataType(item_type)
        case _:
            _json_to_schemas(key, value, schema_dict, date_format, sanitize_symbols)
            return SchemaReference(key)


def _sanitize_symbol(key: str) -> str:
    if len(key) == 0:
        return key
    sanitized_key = re.sub(r"(?![a-zA-Z0-9]).", "_", key)
    if sanitized_key[0].isdigit():
        sanitized_key = "_" + sanitized_key
    return sanitized_key


def _is_valid_date(date_string: str, format_string: str) -> bool:
    regex_pattern = {
        "%Y": r"\d{4}",
        "%m": r"\d{2}",
        "%d": r"\d{2}",
        "%H": r"\d{2}",
        "%M": r"\d{2}",
        "%S": r"\d{2}"
    }
    regex_string = format_string
    for key, value in regex_pattern.items():
        regex_string = regex_string.replace(key, value)
    return bool(re.fullmatch(regex_string, date_string))
