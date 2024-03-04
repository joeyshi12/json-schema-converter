from jdtt.schema import Schema, SchemaDataType, SchemaBasicDataType, \
    SchemaListDataType, SchemaReference, SchemaListDataType, DataType


def schemas_to_typescript(schema_dict: dict[str, Schema]):
    schema_str_list = [_schema_to_typescript(schema) for _, schema in schema_dict.items()]
    return "\n\n".join(schema_str_list)


def _schema_to_typescript(schema: Schema) -> str:
    field_str_list = []
    for field in schema.fields:
        field_str_list.append(f"    {field.name}: {_get_type_symbol(field.data_type)};")
    fields_str = "\n".join(field_str_list)
    return f"export interface {schema.name} {{\n{fields_str}\n}}"


def _get_type_symbol(schema_type: SchemaDataType) -> str:
    match schema_type:
        case SchemaBasicDataType(data_type):
            return _get_data_type_symbol(data_type)
        case SchemaListDataType(item_type):
            return f"{_get_type_symbol(item_type)}[]"
        case SchemaReference(schema_name):
            return schema_name
        case _:
            raise Exception("Invalid schema type: " + schema_type)


def _get_data_type_symbol(data_type: DataType) -> str:
    match data_type:
        case DataType.BOOLEAN:
            return "boolean"
        case DataType.INTEGER:
            return "number"
        case DataType.STRING:
            return "string"
        case DataType.DATE:
            return "Date"
        case _:
            raise Exception("Invalid data type: " + data_type)
