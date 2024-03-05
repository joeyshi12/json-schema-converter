from jdtt.schema import Schema, SchemaDataType, SchemaBasicDataType, \
    SchemaListDataType, SchemaReference, SchemaListDataType, DataType


def schemas_to_java(schema_dict: dict[str, Schema]):
    schema_str_list = [_schema_to_java(schema) for _, schema in schema_dict.items()]
    import_statements_str = "import java.util.Date\n\n"
    return import_statements_str + "\n\n".join(schema_str_list)


def _schema_to_java(schema: Schema) -> str:
    field_str_list = []
    for field in schema.fields:
        field_str_list.append(f"    public {_get_type_symbol(field.data_type)} {field.name};")
    fields_str = "\n".join(field_str_list)
    return f"class {schema.name} {{\n{fields_str}\n}}"


def _get_type_symbol(schema_type: SchemaDataType) -> str:
    match schema_type:
        case SchemaBasicDataType(data_type):
            return _get_data_type_symbol(data_type)
        case SchemaListDataType(item_type):
            return f"List[{_get_type_symbol(item_type)}]"
        case SchemaReference(schema_name):
            return schema_name
        case _:
            raise Exception("Invalid schema type: " + schema_type)


def _get_data_type_symbol(data_type: DataType) -> str:
    match data_type:
        case DataType.BOOLEAN:
            return "boolean"
        case DataType.INTEGER:
            return "int"
        case DataType.INTEGER:
            return "float"
        case DataType.STRING:
            return "String"
        case DataType.DATE:
            return "Date"
        case _:
            return "AnyType"
